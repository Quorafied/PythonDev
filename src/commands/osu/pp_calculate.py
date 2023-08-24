from math import pow, log10
from osu import *

class OsuScore():
    def __init__(self):
        self.scoreId = int(0)
        self.mode = "osu"
        self.userId = int(0)
        self.beatmapId = int(0)
        self.score = int(0)
        self.maxCombo = int(0)
        self.num300 = int(0)
        self.num100 = int(0)
        self.num50 = int(0)
        self.numMiss = int(0)
        self.numGeki = int(0)
        self.numKatu = int(0)
        self.mods = "HD"
        self.beatmap = None

        self.effectiveMissCount = 0
        self.totalValue = 0
        self.aimValue = 0
        self.speedValue = 0
        self.accuracyValue = 0
        self.flashlightValue = 0
        

    def computeValues(self):
        print("Computing Values")
        print("computing effective miss count")
        self.computeEffectiveMissCount(self.beatmap)
        print(self.effectiveMissCount)

        print("\ncomputing aim value")
        self.computeAimValue(self.beatmap)
        print(self.aimValue)

        print("\ncomputing speed value")
        self.computeSpeedValue(self.beatmap)
        print(self.speedValue)

        print("\ncomputing accuracy value")
        self.computeAccuracyValue(self.beatmap)
        print(self.accuracyValue)

        print("\ncomputing total value")
        self.computeTotalValue(self.beatmap)
        print(self.totalValue)

        return self.totalValue

    def newScore(self, score, beatmap):
        print("setting new score")
        self.scoreId = score.id
        self.mode = score.mode
        self.userId = score.user_id
        self.beatmapId = beatmap.id
        self.score = score.score
        self.maxCombo = score.max_combo
        self.num300 = score.statistics.count_300
        self.num100 = score.statistics.count_100
        self.num50 = score.statistics.count_50
        self.numMiss = score.statistics.count_miss
        self.numGeki = score.statistics.count_geki
        self.numKatu = score.statistics.count_katu
        self.mods = score.mods
        self.beatmap = beatmap
        self.beatmapDifficultyAttribute = api.beatmap_attributes(self.beatmapId, mods=self.mods, ruleset="osu")

    def Clamp(self, value, lower_bound, upper_bound):
        return max(lower_bound, min(value, upper_bound))

    def recalculateAccuracy(self, n300, n100, n50, nMiss):
        top = float((n300+n100+n50+nMiss)*(300/300))

        bottom = float(n300*(300/300)) + float(n100*(100/300)) + float(n50*(50/300)) + float(nMiss*(0/300))
        newBottom = float((n300+nMiss)*(300/300)) + float((n100)*(100/300)) + float(n50*(5/300))
        return f"{round((newBottom/top)*100, 2):.2f}"
    
    def recalculateComb(self):
        self.maxCombo = self.beatmapDifficultyAttribute.attributes.max_combo
        self.numMiss = 0

    def checkforMod(self, mod, mods): 
        result = []
        for i in range(0, len(str(mods)) -1, 2):
            result.append(str(mods)[i:i+2])

        if str(mod) in result:
            return True
        else:
            return False

    def TotalValue(self):   
        return self.totalValue
    
    def Accuracy(self):
        if self.TotalHits() == 0:
            return 0

        return self.Clamp(float(self.num50 * 50 + self.num100 * 100 + self.num300 * 300) / (self.TotalHits() * 300), 0.0, 1.0)
        
    def TotalHits(self):
        return self.num50 + self.num100 + self.num300 + self.numMiss
    
    def TotalSuccessfulHits(self):
        return self.num50 + self.num100 + self.num300
    
    def computeEffectiveMissCount(self, beatmap):
        # Guess the number of misses + slider breaks from combo
        comboBasedMissCount = 0.0
        beatmapMaxCombo = self.beatmapDifficultyAttribute.attributes.max_combo

        # If the beatmap has sliders then guess number of misses + slider breaks from combo
        if beatmap.count_sliders > 0:

            fullComboThreshold = float(beatmapMaxCombo - 0.1 * beatmap.count_sliders)
            if self.maxCombo < fullComboThreshold:
                comboBasedMissCount = fullComboThreshold / max(1, self.maxCombo)
        
        # Clamp miss count to maximum amount of possible breaks
        comboBasedMissCount = min(comboBasedMissCount, float(self.num100 + self.num50 + self.numMiss))

        self.effectiveMissCount = max(float(self.numMiss), comboBasedMissCount)

    def computeTotalValue(self, beatmap):
        
        ## Don't count scores made with supposedly unranked mods
        if self.checkforMod("RX", self.mods) or self.checkforMod("V2", self.mods) or self.checkforMod("AP", self.mods):
            self.totalValue = 0
            return
        
        # Multiplier adjusted to keep the final pp value scaled around what it used to be when changing things
        multiplier = 1.14

        if self.checkforMod("NF", self.mods):
            multiplier *= max(0.9, 1.0 - 0.02 * self.effectiveMissCount)

        numTotalHits = int(self.TotalHits())

        if self.checkforMod("SO", self.mods):
            multiplier *= 1.0 - pow(beatmap.count_sliders / float(numTotalHits), 0.85)

        print(f"multiplier: {multiplier}")

        self.totalValue = pow(
                            pow(self.aimValue, 1.1) +
                                pow(self.speedValue, 1.1) +
                                pow(self.accuracyValue, 1.1) +
                                pow(self.flashlightValue, 1.1),
                            1.0 / 1.1) * multiplier
                        

    def computeAimValue(self, beatmap):
        self.aimValue = pow(5.0 * max(1.0, self.beatmapDifficultyAttribute.attributes.aim_difficulty / 0.0675) - 4.0, 3.0) / 100000.0

        numTotalHits = int(self.TotalHits())

        lengthBonus = float(0.95 + 0.4 * min(1.0, float(numTotalHits) / 2000.0) + (log10(float(numTotalHits) / 2000.0) * 0.5 if numTotalHits > 2000 else 0.0))

        self.aimValue *= lengthBonus

        # Penalize misses by assessing # of misses relative to the total # of objects. Default a 3% reduction for any # of misses
        if self.effectiveMissCount > 0:
            self.aimValue *= 0.97 * pow(1.0 - pow(self.effectiveMissCount / float(numTotalHits), 0.775), self.effectiveMissCount)

        self.aimValue *= self.getComboScalingFactor(beatmap)

        approachRate = float(self.beatmapDifficultyAttribute.attributes.approach_rate)
        approachRateFactor = 0.0
        if approachRate > 10.33:
            approachRateFactor = 0.3 * (approachRate - 10.33)
        elif approachRate < 8.0:
            approachRateFactor = 0.05 * (8.0 - approachRate)

        self.aimValue *= 1.0 + approachRateFactor * lengthBonus

        # We want to give more reward for lower AR when it comes to aim and HD. This nerfs high AR and buffs lower AR.
        if self.checkforMod("HD", self.mods):
            self.aimValue *= 1.0 + 0.04 * (12.0 - approachRate)

        # We assume 15% of sliders in a map are difficult since there's no way to tell from the performance calculator.
        estimateDifficultSliders = float(beatmap.count_sliders * 0.15)

        if beatmap.count_sliders > 0:
            maxCombo = float(self.beatmapDifficultyAttribute.attributes.max_combo)
            estimateSliderEndsDropped = float(min(max(min(float(self.num100 + self.num50 + self.numMiss), maxCombo - self.maxCombo), 0.0), estimateDifficultSliders))
            sliderFactor = float(self.beatmapDifficultyAttribute.attributes.slider_factor)
            sliderNerfFactor = (1.0 - sliderFactor) * pow(1.0 - estimateSliderEndsDropped / estimateDifficultSliders, 3) + sliderFactor
            self.aimValue *= sliderNerfFactor

        self.aimValue *= self.Accuracy()

        # It is important to consider accuracy difficulty when scaling with accuracy.
        self.aimValue *= 0.98 + (pow(self.beatmapDifficultyAttribute.attributes.overall_difficulty, 2) / 2500)

    def computeSpeedValue(self, beatmap):
        self.speedValue = pow(5.0 * max(1.0, self.beatmapDifficultyAttribute.attributes.speed_difficulty / 0.0675) - 4.0, 3.0) / 100000.0

        numTotalHits = int(self.TotalHits())

        lengthBonus = 0.95 + 0.4 * min(1.0, float(numTotalHits) / 2000.0) + (log10(float(numTotalHits) / 2000.0) * 0.5 if numTotalHits > 2000 else 0.0)

        self.speedValue *= lengthBonus

        # Penalize misses by assessing # of misses relative to the total # of objects. Default a #% reduction for any # of misses.
        if self.effectiveMissCount > 0:
            self.speedValue *= 0.97 *pow(1.0 - pow(self.effectiveMissCount / float(numTotalHits), 0.775), pow(self.effectiveMissCount, 0.875))


        self.speedValue *= self.getComboScalingFactor(beatmap)


        approachRate = self.beatmapDifficultyAttribute.attributes.approach_rate
        approachRateFactor = 0.0


        if approachRate > 10.33:
            approachRateFactor = 0.3 * (approachRate - 10.33)


        self.speedValue *= 1.0 + approachRateFactor * lengthBonus # Buff for longer maps with high AR


        # We want to give more reward for lower AR when it comes to speed and HD. This nerfs high AR and buffs lower AR.
        if self.checkforMod("HD", self.mods):
            self.speedValue *= 1.0 + 0.04 * (12.0 - approachRate)

    
        # Calculate accuracy assuming the worst case scenario
        relevantTotalDiff = float(numTotalHits) - self.beatmapDifficultyAttribute.attributes.speed_note_count
        relevantCountGreat = max(0.0, self.num300 - relevantTotalDiff)
        relevantCountOk = max(0.0, self.num100 - max(0.0, relevantTotalDiff - self.num300))
        relevantCountMeh = max(0.0, self.num50 - max(0.0, relevantTotalDiff - self.num300 - self.num100))
        relevantAccuracy = 0.0 if self.beatmapDifficultyAttribute.attributes.speed_note_count == 0.0 else (relevantCountGreat * 6.0 + relevantCountOk * 2.0 + relevantCountMeh) / (self.beatmapDifficultyAttribute.attributes.speed_note_count * 6.0)

        # Scale the speed value with accuracy and OD.
        self.speedValue *= (0.95 + pow(self.beatmapDifficultyAttribute.attributes.overall_difficulty, 2) / 750) * pow((self.Accuracy() + relevantAccuracy) / 2.0, (14.5 - max(self.beatmapDifficultyAttribute.attributes.overall_difficulty, 8.0)) / 2)

        # Scale the speed value with # of 50s to punish doubletapping.
        self.speedValue *= pow(0.99, 0.0 if self.num50 < numTotalHits / 500.0 else self.num50 - numTotalHits / 500.0)

    def computeAccuracyValue(self, beatmap):
        
        # This percentage only considers HitCircles of any value - in this part of the calculation we focus on hitting the timing hit window.
        betterAccuracyPercetange = 0.0

        numHitObjectsWithAccuracy = 0.0

        if self.checkforMod("V2", self.mods):
            numHitObjectsWithAccuracy = self.TotalHits()
            betterAccuracyPercetange = self.Accuracy()
        
        # Either ScoreV1 or some unknown value. Let's default to previous behaviour.
        else:
            numHitObjectsWithAccuracy = beatmap.count_circles
            if numHitObjectsWithAccuracy > 0:
                betterAccuracyPercetange = float((self.num300 - (self.TotalHits() - numHitObjectsWithAccuracy)) * 6 + self.num100 * 2 + self.num50) / (numHitObjectsWithAccuracy * 6)
            else:
                betterAccuracyPercetange = 0

            # It is possible to reach a negative accuracy with this formula. Cap it at zero - zero points
            if betterAccuracyPercetange < 0:
                betterAccuracyPercetange = 0
        
        # Lots of arbitrary values from testing.
        # Considering to use derivation from perfect accuracy in a probabilistic manner - assume normal distribution.
        self.accuracyValue = pow(1.52163, self.beatmapDifficultyAttribute.attributes.overall_difficulty) * pow(betterAccuracyPercetange, 24) * 2.83

        # Bonus for many hitcircles - it's harder to keep good accuracy up for longer.
        self.accuracyValue *= min(1.15, float(pow(numHitObjectsWithAccuracy / 1000.0 , 0.3)))

        if self.checkforMod("HD", self.mods):
            self.accuracyValue *= 1.08
        
        if self.checkforMod("FL", self.mods):
            self.accuracyValue *= 1.02
    
    def computeFlashlightValue(self, beatmap):
        self.flashlightValue = 0.0

        if self.checkforMod("FL", self.mods) is False:
            return

        self.flashlightValue = pow(self.beatmapDifficultyAttribute.attributes.flashlight_difficulty, 2.0) * 25.0

        numTotalHits = int(self.TotalHits())

        # Penalize misses by assessing # of misses relative to the total # of objects. Default a 3% reduction for any # of misses.
        if self.effectiveMissCount > 0:
            self.flashlightValue *= 0.97 * pow(1 - pow(self.effectiveMissCount / float(numTotalHits), 0.775), pow(self.effectiveMissCount, 0.875))

        self.flashlightValue *= self.getComboScalingFactor(beatmap)

        # Account for shorter maps having a higher ratio of 0 combo/100 combo flashlight radius.
        self.flashlightValue *= 0.7 + 0.1 * min(1.0, float(numTotalHits)/ 200.0) + (0.2 * min(1.0, (float(numTotalHits) - 200) / 200) if numTotalHits > 200 else 0.0)

        # Scale the flashlight value with accuracy _slightly_.
        self.flashlightValue *= 0.5 + self.Accuracy() / 2.0

        # It is important to also consider accuracy difficulty when doing that.
        self.flashlightValue *= 0.98 + pow(self.beatmapDifficultyAttribute.attributes.overall_difficulty, 2.0) / 2500.0

    def getComboScalingFactor(self, beatmap):
        maxCombo = float(self.beatmapDifficultyAttribute.attributes.max_combo)
        if maxCombo > 0:
            return min(float(pow(self.maxCombo, 0.8) / pow(maxCombo, 0.8)), 1.0)
        return 1.0

ppCalculator = OsuScore()




