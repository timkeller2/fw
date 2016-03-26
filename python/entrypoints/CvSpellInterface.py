#Spell system and FfH specific callout python functions
#All code by Kael, all bugs by woodelf

from CvPythonExtensions import *
import CvUtil
import Popup as PyPopup
import CvScreensInterface
import sys
import PyHelpers
import CustomFunctions
import ScenarioFunctions
import pickle
import math

PyInfo = PyHelpers.PyInfo
PyPlayer = PyHelpers.PyPlayer
gc = CyGlobalContext()
cf = CustomFunctions.CustomFunctions()
sf = ScenarioFunctions.ScenarioFunctions()

def cast(argsList):
	pCaster, eSpell = argsList
	spell = gc.getSpellInfo(eSpell)
	eval(spell.getPyResult())

def canCast(argsList):
	pCaster, eSpell = argsList
	spell = gc.getSpellInfo(eSpell)
	return eval(spell.getPyRequirement())

def effect(argsList):
	pCaster, eProm = argsList
	prom = gc.getPromotionInfo(eProm)
	eval(prom.getPyPerTurn())

def atRange(argsList):
	pCaster, pPlot, eImp = argsList
	imp = gc.getImprovementInfo(eImp)
	eval(imp.getPythonAtRange())

def onMove(argsList):
	pCaster, pPlot, eImp = argsList
	imp = gc.getImprovementInfo(eImp)
	eval(imp.getPythonOnMove())

def onMoveFeature(argsList):
	pCaster, pPlot, eFeature = argsList
	feature = gc.getFeatureInfo(eFeature)
	eval(feature.getPythonOnMove())

def vote(argsList):
	eVote, int = argsList
	vote = gc.getVoteInfo(eVote)
	eval(vote.getPyResult())

def miscast(argsList):
	pCaster, eSpell = argsList
	spell = gc.getSpellInfo(eSpell)
	eval(spell.getPyMiscast())

def postCombatLost(argsList):
	pCaster, pOpponent = argsList
	unit = gc.getUnitInfo(pCaster.getUnitType())
	eval(unit.getPyPostCombatLost())

def postCombatWon(argsList):
	pCaster, pOpponent = argsList
	unit = gc.getUnitInfo(pCaster.getUnitType())
	eval(unit.getPyPostCombatWon())

def findClearPlot(pUnit, plot):
	BestPlot = -1
	iBestPlot = 0
	if pUnit == -1:
		iX = plot.getX()
		iY = plot.getY()
		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				iCurrentPlot = 0
				pPlot = CyMap().plot(iiX,iiY)
				if pPlot.getNumUnits() == 0:
					if (pPlot.isWater() == plot.isWater() and pPlot.isPeak() == False and pPlot.isCity() == False):
						iCurrentPlot = iCurrentPlot + 5
				if iCurrentPlot >= 1:
					iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum(5, "findClearPlot")
					if iCurrentPlot >= iBestPlot:
						BestPlot = pPlot
						iBestPlot = iCurrentPlot
		return BestPlot
	iX = pUnit.getX()
	iY = pUnit.getY()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			iCurrentPlot = 0
			pPlot = CyMap().plot(iiX,iiY)
			if pPlot.getNumUnits() == 0:
				if pUnit.canMoveOrAttackInto(pPlot, False):
					iCurrentPlot = iCurrentPlot + 5
			for i in range(pPlot.getNumUnits()):
				if pPlot.getUnit(i).getOwner() == pUnit.getOwner():
					if pUnit.canMoveOrAttackInto(pPlot, False):
						iCurrentPlot = iCurrentPlot + 15
			if pPlot.isCity():
				if pPlot.getPlotCity().getOwner() == pUnit.getOwner():
					iCurrentPlot = iCurrentPlot + 50
			if (iX == iiX and iY == iiY):
				iCurrentPlot = 0
			if iCurrentPlot >= 1:
				iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum(5, "findClearPlot")
				if iCurrentPlot >= iBestPlot:
					BestPlot = pPlot
					iBestPlot = iCurrentPlot
	return BestPlot

def postCombatConsumePaladin(pCaster, pOpponent):
	if (pOpponent.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_PALADIN')):
		pCaster.setDamage(0, pCaster.getOwner())
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_CONSUME_PALADIN", ()),'',1,'Art/Interface/Buttons/Units/Beast of Agares.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)

def postCombatDonal(pCaster, pOpponent):
	if (pOpponent.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON')) or pOpponent.isHasPromotion(gc.getInfoTypeForString('PROMOTION_UNDEAD'))):
		pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RECRUITER'), True)

def postCombatExplode(pCaster, pOpponent):
	iX = pCaster.getX()
	iY = pCaster.getY()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			if not (iiX == iX and iiY == iY):
				pPlot = CyMap().plot(iiX,iiY)
				if pPlot.isNone() == False:
					if (pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FOREST') or pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_JUNGLE') or pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FOREST_NEW')):
						if CyGame().getSorenRandNum(100, "Flames Spread") <= gc.getDefineINT('FLAMES_SPREAD_CHANCE'):
							bValid = True
							iImprovement = pPlot.getImprovementType()
							if iImprovement != -1 :
								if gc.getImprovementInfo(iImprovement).isPermanent() :
									bValid = False
							if bValid:
								pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_SMOKE'))
					for i in range(pPlot.getNumUnits()):
						pUnit = pPlot.getUnit(i)
						pUnit.doDamage(10, 100, pCaster, gc.getInfoTypeForString('DAMAGE_FIRE'), false)

def postCombatHeal50(pCaster, pOpponent):
	if pCaster.getDamage() > 0:
		pCaster.setDamage(pCaster.getDamage() / 2, pCaster.getOwner())

def postCombatIra(pCaster, pOpponent):
	if pOpponent.isAlive():
		if pCaster.baseCombatStr() < 32:
			pCaster.setBaseCombatStr(pCaster.baseCombatStr() - 3)
			pCaster.setBaseCombatStrDefense(pCaster.baseCombatStrDefense() - 3)

def postCombatMimic(pCaster, pOpponent):
	iBronze = gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS')
	iChanneling3 = gc.getInfoTypeForString('PROMOTION_CHANNELING3')
	iDivine = gc.getInfoTypeForString('PROMOTION_DIVINE')
	iGreatCommander = gc.getInfoTypeForString('PROMOTION_GREAT_COMMANDER')
	iIron = gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')
	iMithril = gc.getInfoTypeForString('PROMOTION_MITHRIL_WEAPONS')
	listProms = []
	iCount = 0
	for iProm in range(gc.getNumPromotionInfos()):
		if pCaster.isHasPromotion(iProm):
			iCount += 1
		else:
			if (pOpponent.isHasPromotion(iProm)):
				if gc.getPromotionInfo(iProm).isEquipment() == False:
					if (iProm != iChanneling3 and iProm != iDivine and iProm != iBronze and iProm != iIron and iProm != iMithril and iProm != iGreatCommander):
						if gc.getPromotionInfo(iProm).isRace() == false:
							listProms.append(iProm)
	if len(listProms) > 0:
		iCount += 1
		iRnd = CyGame().getSorenRandNum(len(listProms), "Mimic")
		pCaster.setHasPromotion(listProms[iRnd], True)
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PROMOTION_STOLEN", ()),'',1,gc.getPromotionInfo(listProms[iRnd]).getButton(),ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
	if iCount >= 20:
		pPlayer = gc.getPlayer(pCaster.getOwner())
		if pPlayer.isHuman():
			t = "TROPHY_FEAT_MIMIC_20"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatAcheron(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_ACHERON"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatArs(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_ARS"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatAuricAscendedLost(pCaster, pOpponent):
	iPlayer = pCaster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	for iTrait in range(gc.getNumTraitInfos()):
		if pPlayer.hasTrait(iTrait):
			pPlayer.setHasTrait(iTrait, False)
	if pOpponent.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GODSLAYER')):
		pOppPlayer = gc.getPlayer(pOpponent.getOwner())
		if pOppPlayer.isHuman():
			t = "TROPHY_FEAT_GODSLAYER"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatAuricAscendedWon(pCaster, pOpponent):
	if pOpponent.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GODSLAYER')):
		iPlayer = pCaster.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		for iTrait in range(gc.getNumTraitInfos()):
			if pPlayer.hasTrait(iTrait):
				pPlayer.setHasTrait(iTrait, False)
		pCaster.kill(True, pOpponent.getOwner())
		pOppPlayer = gc.getPlayer(pOpponent.getOwner())
		if pOppPlayer.isHuman():
			t = "TROPHY_FEAT_GODSLAYER"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatBasium(pCaster, pOpponent):
	if not pCaster.isImmortal():
		iPlayer = pCaster.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		for iTrait in range(gc.getNumTraitInfos()):
			if pPlayer.hasTrait(iTrait):
				pPlayer.setHasTrait(iTrait, False)
		pOppPlayer = gc.getPlayer(pOpponent.getOwner())
		if pOppPlayer.isHuman():
			t = "TROPHY_DEFEATED_BASIUM"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatBrigitHeld(pCaster, pOpponent):
	pPlot = pCaster.plot()
	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_RING_OF_CARCER'):
		pPlot.setImprovementType(-1)
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_FEAT_RESCUE_BRIGIT"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatBuboes(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_BUBOES"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatHyborem(pCaster, pOpponent):
	if not pCaster.isImmortal():
		iPlayer = pCaster.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		for iTrait in range(gc.getNumTraitInfos()):
			if iTrait != gc.getInfoTypeForString('TRAIT_FALLOW'):
				if pPlayer.hasTrait(iTrait):
					pPlayer.setHasTrait(iTrait, False)
		pOppPlayer = gc.getPlayer(pOpponent.getOwner())
		if pOppPlayer.isHuman():
			t = "TROPHY_DEFEATED_HYBOREM"
			if not CyGame().isHasTrophy(t):
				CyGame().changeTrophyValue(t, 1)

def postCombatLeviathan(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_LEVIATHAN"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatOrthus(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_ORTHUS"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatStephanos(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_STEPHANOS"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatTreant(pCaster, pOpponent):
	pPlot = pCaster.plot()
	if pPlot.getFeatureType() == -1:
		if pPlot.canHaveFeature(gc.getInfoTypeForString('FEATURE_FOREST_NEW')):
			pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_FOREST_NEW'), 0)

def postCombatYersinia(pCaster, pOpponent):
	pPlayer = gc.getPlayer(pOpponent.getOwner())
	if pPlayer.isHuman():
		t = "TROPHY_DEFEATED_YERSINIA"
		if not CyGame().isHasTrophy(t):
			CyGame().changeTrophyValue(t, 1)

def postCombatReduceCombat1(pCaster, pOpponent):
	if pOpponent.isAlive():
		if pCaster.baseCombatStr() > 5:
			pCaster.setBaseCombatStr(pCaster.baseCombatStr() - 5)
			pCaster.setBaseCombatStrDefense(pCaster.baseCombatStrDefense() - 5)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_STRENGTH_REDUCED", ()),'',1,'Art/Interface/Buttons/Units/Repentant Angel.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def postCombatReducePopulation(pCaster, pOpponent):
	pPlot = pOpponent.plot()
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getPopulation() > 1:
			pCity.changePopulation(-1)
			CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POPULATION_REDUCED", ()),'',1,'Art/Interface/Buttons/Units/Angel of Death.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)

def postCombatLostSailorsDirge(pCaster, pOpponent):
	iPlayer = pOpponent.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_SAILORS_DIRGE_DEFEATED')
	triggerData = pPlayer.initTriggeredData(iEvent, true, -1, pCaster.getX(), pCaster.getY(), iPlayer, -1, -1, -1, -1, -1)

def postCombatSplit(pCaster, pOpponent):
	if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK')) == False:
		pPlayer = gc.getPlayer(pCaster.getOwner())
		iUnit = pCaster.getUnitType()
		newUnit = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit2 = pPlayer.initUnit(iUnit, pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), False)
		newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG'), False)
		newUnit.setDamage(25, -1)
		newUnit2.setDamage(25, -1)
		if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_STRONG')) == False:
			newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)
			newUnit2.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WEAK'), True)
		newUnit.setDuration(pCaster.getDuration())
		newUnit2.setDuration(pCaster.getDuration())
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_SPLIT", ()),'',1,gc.getUnitInfo(iUnit).getButton(),ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def postCombatWolfRider(pCaster, pOpponent):
	if (pOpponent.getUnitType() == gc.getInfoTypeForString('UNIT_WOLF') or pOpponent.getUnitType() == gc.getInfoTypeForString('UNIT_WOLF_PACK')):
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WOLF_RIDER", ()),'',1,'Art/Interface/Buttons/Units/Wolf Rider.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
		pPlayer = gc.getPlayer(pCaster.getOwner())
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOLF_RIDER'), pCaster.getX(), pCaster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.convert(pCaster)

def reqAddToFleshGolem(caster):
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL')):
		return false
	if caster.isImmuneToMagic():
		return False
	return True

def spellAddToFleshGolem(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iChanneling = gc.getInfoTypeForString('PROMOTION_CHANNELING')
	iChanneling2 = gc.getInfoTypeForString('PROMOTION_CHANNELING2')
	iChanneling3 = gc.getInfoTypeForString('PROMOTION_CHANNELING3')
	iDivine = gc.getInfoTypeForString('PROMOTION_DIVINE')
	iFleshGolem = gc.getInfoTypeForString('UNITCLASS_FLESH_GOLEM')
	pFleshGolem = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitClassType() == iFleshGolem):
			pFleshGolem = pUnit
	if pFleshGolem != -1:
		if caster.baseCombatStr() > pFleshGolem.baseCombatStr():
			pFleshGolem.setBaseCombatStr(pFleshGolem.baseCombatStr() + 1)
		if caster.baseCombatStrDefense() > pFleshGolem.baseCombatStrDefense():
			pFleshGolem.setBaseCombatStrDefense(pFleshGolem.baseCombatStrDefense() + 1)
		for iCount in range(gc.getNumPromotionInfos()):
			if (caster.isHasPromotion(iCount)):
				if (iCount != iChanneling and iCount != iChanneling2 and iCount != iChanneling3 and iCount != iDivine):
					if not gc.getPromotionInfo(iCount).isRace():
						if gc.getPromotionInfo(iCount).getBonusPrereq() == -1:
							if gc.getPromotionInfo(iCount).getPromotionPrereqAnd() != iChanneling2:
								if gc.getPromotionInfo(iCount).getPromotionPrereqAnd() != iChanneling3:
									if gc.getPromotionInfo(iCount).isEquipment() == False:
										pFleshGolem.setHasPromotion(iCount, true)
		if pFleshGolem.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MITHRIL_WEAPONS')):
			pFleshGolem.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS'), False)
			pFleshGolem.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), False)
		if pFleshGolem.isHasPromotion(gc.getInfoTypeForString('PROMOTION_IRON_WEAPONS')):
			pFleshGolem.setHasPromotion(gc.getInfoTypeForString('PROMOTION_BRONZE_WEAPONS'), False)
		if pFleshGolem.baseCombatStr() >= 15:
			if pPlayer.isHuman():
				t = "TROPHY_FEAT_FLESH_GOLEM_15"
				if not CyGame().isHasTrophy(t):
					CyGame().changeTrophyValue(t, 1)

def reqAddToFreakShowHuman(caster):
	if caster.getRace() != -1:
		return False
	return True

def reqAddToWolfPack(caster):
	pPlot = caster.plot()
	iWolfPack = gc.getInfoTypeForString('UNIT_WOLF_PACK')
	iEmpower5 = gc.getInfoTypeForString('PROMOTION_EMPOWER5')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == iWolfPack:
			if pUnit.getOwner() == caster.getOwner():
				if not pUnit.isHasPromotion(iEmpower5):
					return True
	return False

def spellAddToWolfPack(caster):
	pPlot = caster.plot()
	iWolfPack = gc.getInfoTypeForString('UNIT_WOLF_PACK')
	iEmpower1 = gc.getInfoTypeForString('PROMOTION_EMPOWER1')
	iEmpower2 = gc.getInfoTypeForString('PROMOTION_EMPOWER2')
	iEmpower3 = gc.getInfoTypeForString('PROMOTION_EMPOWER3')
	iEmpower4 = gc.getInfoTypeForString('PROMOTION_EMPOWER4')
	iEmpower5 = gc.getInfoTypeForString('PROMOTION_EMPOWER5')
	bValid = True
	for i in range(pPlot.getNumUnits()):
		if bValid:
			pUnit = pPlot.getUnit(i)
			if pUnit.getUnitType() == iWolfPack:
				if pUnit.getOwner() == caster.getOwner():
					iProm = -1
					if not pUnit.isHasPromotion(iEmpower5):
						iProm = iEmpower5
					if not pUnit.isHasPromotion(iEmpower4):
						iProm = iEmpower4
					if not pUnit.isHasPromotion(iEmpower3):
						iProm = iEmpower3
					if not pUnit.isHasPromotion(iEmpower2):
						iProm = iEmpower2
					if not pUnit.isHasPromotion(iEmpower1):
						iProm = iEmpower1
					if iProm != -1:
						pUnit.setHasPromotion(iProm, True)
						bValid = False

def reqArcaneLacuna(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	manaTypes = [ 'BONUS_MANA_AIR','BONUS_MANA_BODY','BONUS_MANA_CHAOS','BONUS_MANA_DEATH','BONUS_MANA_EARTH','BONUS_MANA_ENCHANTMENT','BONUS_MANA_ENTROPY','BONUS_MANA_FIRE','BONUS_MANA_LAW','BONUS_MANA_LIFE','BONUS_MANA_METAMAGIC','BONUS_MANA_MIND','BONUS_MANA_NATURE','BONUS_MANA_SHADOW','BONUS_MANA_SPIRIT','BONUS_MANA_SUN','BONUS_MANA_WATER' ]
	iCount = 0
	for szBonus in manaTypes:
		iBonus = gc.getInfoTypeForString(szBonus)
		iCount += CyMap().getNumBonuses(iBonus)
	if iCount == 0:
		return False
	if pPlayer.isHuman() == False:
		if iCount < 7:
			return False
	return True

def spellArcaneLacuna(caster):
	manaTypes = [ 'BONUS_MANA_AIR','BONUS_MANA_BODY','BONUS_MANA_CHAOS','BONUS_MANA_DEATH','BONUS_MANA_EARTH','BONUS_MANA_ENCHANTMENT','BONUS_MANA_ENTROPY','BONUS_MANA_FIRE','BONUS_MANA_LAW','BONUS_MANA_LIFE','BONUS_MANA_METAMAGIC','BONUS_MANA_MIND','BONUS_MANA_NATURE','BONUS_MANA_SHADOW','BONUS_MANA_SPIRIT','BONUS_MANA_SUN','BONUS_MANA_WATER' ]
	iAdept = gc.getInfoTypeForString('UNITCOMBAT_ADEPT')
	iCount = 0
	pPlayer = gc.getPlayer(caster.getOwner())
	for szBonus in manaTypes:
		iBonus = gc.getInfoTypeForString(szBonus)
		iCount += CyMap().getNumBonuses(iBonus)
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.getUnitCombatType() == iAdept:
			pUnit.changeExperience(iCount, -1, False, False, False)
	iDelay = 20
	if CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
		iDelay = 14
	if CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
		iDelay = 30
	if CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
		iDelay = 60
	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.isAlive():
			if pPlayer2.getTeam() != pPlayer.getTeam():
				pPlayer2.changeDisableSpellcasting(iDelay)

def reqArdor(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getGreatPeopleCreated() == 0:
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getGreatPeopleCreated() < 5:
			return False
	return True

def spellArdor(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.setGreatPeopleCreated(0)
	pPlayer.setGreatPeopleThresholdModifier(0)

def reqArenaBattle(caster):
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_MELEE'):
		return True
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_RECON'):
		return True
	if caster.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_SLAVE'):
		return True
	return False

def spellArenaBattle(caster):
	pCity = caster.plot().getPlotCity()
	pCity.changeHappinessTimer(3)
	if CyGame().getSorenRandNum(100, "Arena Battle") < 50:
		caster.changeExperience(CyGame().getSorenRandNum(6, "Arena Battle") + 1, -1, False, False, False)
		caster.setDamage(25, caster.getOwner())
		CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_WIN", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
		if caster.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_SLAVE'):
			pPlayer = gc.getPlayer(caster.getOwner())
			newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WARRIOR'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(caster)
	else:
		CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_ARENA_LOSE", ()),'',1,'Art/Interface/Buttons/Buildings/Arena.dds',ColorTypes(7),caster.getX(),caster.getY(),True,True)
		caster.kill(True, PlayerTypes.NO_PLAYER)

def reqCallBlizzard(caster):
	iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')
	pPlot = caster.plot()
	if pPlot.getFeatureType() == iBlizzard:
		return False
	if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT'):
		return False
	iX = caster.getX()
	iY = caster.getY()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			if pPlot.getFeatureType() == iBlizzard:
				return True
	return False

def spellCallBlizzard(caster):
	iBlizzard = gc.getInfoTypeForString('FEATURE_BLIZZARD')
	iTundra = gc.getInfoTypeForString('TERRAIN_TUNDRA')
	iX = caster.getX()
	iY = caster.getY()
	pBlizPlot = -1
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			if pPlot.getFeatureType() == iBlizzard:
				pBlizPlot = pPlot
	if pBlizPlot != -1:
		pBlizPlot.setFeatureType(-1, -1)
	pPlot = caster.plot()
	pPlot.setFeatureType(iBlizzard, 0)
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_GRASS'):
		pPlot.setTerrainType(iTundra,True,True)
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS'):
		pPlot.setTerrainType(iTundra,True,True)
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT'):
		pPlot.setTerrainType(iTundra,True,True)

def reqCallForm(caster):
	if caster.getSummoner() == -1:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	pUnit = pPlayer.getUnit(caster.getSummoner())
	pPlot = caster.plot()
	if not pUnit.canMoveInto(pPlot, False, False, False):
		return False
	return True

def spellCallForm(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pUnit = pPlayer.getUnit(caster.getSummoner())
	pPlot = caster.plot()
	pUnit.setXY(pPlot.getX(), pPlot.getY(), false, true, true)

def reqCallOfTheGrave(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	eTeam = gc.getTeam(pPlayer.getTeam())
	iGraveyard = gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD')
	iUndead = gc.getInfoTypeForString('PROMOTION_UNDEAD')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				p2Player = gc.getPlayer(pUnit.getOwner())
				e2Team = p2Player.getTeam()
				if eTeam.isAtWar(e2Team) == True:
					return True
				if pUnit.getRace() == iUndead:
					if pUnit.getDamage() != 0:
						return True
				if pPlot.getImprovementType() == iGraveyard:
					return True
	return False

def spellCallOfTheGrave(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iX = caster.getX()
	iY = caster.getY()
	eTeam = gc.getTeam(pPlayer.getTeam())
	iGraveyard = gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD')
	iUndead = gc.getInfoTypeForString('PROMOTION_UNDEAD')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot = CyMap().plot(iiX,iiY)
			bValid = False
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				p2Player = gc.getPlayer(pUnit.getOwner())
				e2Team = p2Player.getTeam()
				if eTeam.isAtWar(e2Team) == True:
					pUnit.doDamage(40, 100, caster, gc.getInfoTypeForString('DAMAGE_DEATH'), true)
					bValid = True
				else:
					if pUnit.getRace() == iUndead:
						if pUnit.getDamage() != 0:
							pUnit.setDamage(0, caster.getOwner())
				if pPlot.getImprovementType() == iGraveyard:
					pPlot.setImprovementType(-1)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WRAITH'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WRAITH'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WRAITH'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
					bValid = True
			if bValid:
				CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SACRIFICE'),pPlot.getPoint())

def reqCommanderJoin(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_GREAT_COMMANDER')):
		return False
	iCommander = gc.getInfoTypeForString('UNITCLASS_COMMANDER')
	pCommander = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitClassType() == iCommander):
			pCommander = pUnit
	if pCommander == -1:
		return False
	if pCommander.isHasCasted():
		return False
	if pPlayer.isHuman() == False:
		if caster.baseCombatStr() <= 5:
			return False
	return True

def spellCommanderJoin(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iCommander = gc.getInfoTypeForString('UNITCLASS_COMMANDER')
	pCommander = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitClassType() == iCommander):
			pCommander = pUnit
	if pCommander != -1:
		pCommander.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GOLEM'), True)
		pCommander.kill(False, PlayerTypes.NO_PLAYER)

def spellCommanderJoinDecius(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iDecius = gc.getInfoTypeForString('UNIT_DECIUS')
	pCommander = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (caster.getOwner() == pUnit.getOwner() and pUnit.getUnitType() == iDecius):
			pCommander = pUnit
	if pCommander != -1:
		caster.setScenarioCounter(iDecius)
		pCommander.setHasPromotion(gc.getInfoTypeForString('PROMOTION_GOLEM'), True)
		pCommander.kill(False, PlayerTypes.NO_PLAYER)

def spellCommanderSplit(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCommander = gc.getInfoTypeForString('UNIT_COMMANDER')
	if caster.getScenarioCounter() == gc.getInfoTypeForString('UNIT_DECIUS'):
		iCommander = gc.getInfoTypeForString('UNIT_DECIUS')
		caster.setScenarioCounter(-1)
	newUnit = pPlayer.initUnit(iCommander, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqConvertCityBasium(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if pCity.getOwner() == caster.getOwner():
		return False
	return True

def spellConvertCityBasium(caster):
	pCity = caster.plot().getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.acquireCity(pCity,false,false)
	pCity = caster.plot().getPlotCity()
	pCity.changeCulture(iPlayer, 300, True)

def reqConvertCityRantine(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if pCity.getOwner() == caster.getOwner():
		return False
	if pCity.getOwner() != gc.getBARBARIAN_PLAYER():
		return False
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == gc.getBARBARIAN_PLAYER():
			if pUnit.baseCombatStr() > caster.baseCombatStr():
				return False
	return True

def spellConvertCityRantine(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.acquireCity(pCity,false,false)

def spellCreateBatteringRam(caster):
	pPlot = caster.plot()
	pPlot.setFeatureType(-1, -1)

def reqCreateDenBear(caster):
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_LAIRS):
		return False
	iImprovement = gc.getInfoTypeForString('IMPROVEMENT_BEAR_DEN')
	if caster.getDamage() > 0:
		return False
	pPlot = caster.plot()
	if pPlot.isOwned():
		return False
	if pPlot.getNumUnits() != 1:
		return False
	if pPlot.getImprovementType() != -1:
		return False
	if pPlot.canHaveImprovement(iImprovement, caster.getOwner(), true) == False:
		return False
	iX = pPlot.getX()
	iY = pPlot.getY()
	for iiX in range(iX-4, iX+5, 1):
		for iiY in range(iY-4, iY+5, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if pPlot2.getImprovementType() == iImprovement:
				return False
	return True

def spellCreateDenBear(caster):
	pPlot = caster.plot()
	iImprovement = gc.getInfoTypeForString('IMPROVEMENT_BEAR_DEN')
	iUnit = gc.getInfoTypeForString('UNIT_BEAR')
	pPlot.setImprovementType(iImprovement)
	pPlot2 = findClearPlot(-1, caster.plot())
	if pPlot2 != -1:
		caster.setXY(pPlot2.getX(), pPlot2.getY(), false, true, true)
		pPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.convert(caster)

def reqCreateDenLion(caster):
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_LAIRS):
		return False
	iImprovement = gc.getInfoTypeForString('IMPROVEMENT_LION_DEN')
	if caster.getDamage() > 0:
		return False
	pPlot = caster.plot()
	if pPlot.isOwned():
		return False
	if pPlot.getNumUnits() != 1:
		return False
	if pPlot.getImprovementType() != -1:
		return False
	if pPlot.canHaveImprovement(iImprovement, caster.getOwner(), true) == False:
		return False
	iX = pPlot.getX()
	iY = pPlot.getY()
	for iiX in range(iX-4, iX+5, 1):
		for iiY in range(iY-4, iY+5, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if pPlot2.getImprovementType() == iImprovement:
				return False
	return True

def spellCreateDenLion(caster):
	pPlot = caster.plot()
	iImprovement = gc.getInfoTypeForString('IMPROVEMENT_LION_DEN')
	iUnit = gc.getInfoTypeForString('UNIT_LION')
	pPlot.setImprovementType(iImprovement)
	pPlot2 = findClearPlot(-1, caster.plot())
	if pPlot2 != -1:
		caster.setXY(pPlot2.getX(), pPlot2.getY(), false, true, true)
		pPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.convert(caster)

def reqCrewBuccaneers(caster):
	pPlot = caster.plot()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BUCCANEERS')):
		return False
	if caster.maxMoves() <= 1:
		return False
	if caster.baseCombatStr() < 1:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == false:
		iUnit = caster.getUnitType()
		if (iUnit != gc.getInfoTypeForString('UNIT_FRIGATE') and iUnit != gc.getInfoTypeForString('UNIT_MAN_O_WAR')):
			return false
	return true

def reqCrewLongshoremen(caster):
	pPlot = caster.plot()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LONGSHOREMEN')):
		return False
#	if (PyInfo.UnitInfo(caster.getUnitType()).getCargoSpace() == 0 and caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_EXPANDED_HULL')) == False):
#		return False
	if caster.cargoSpaceAvailable(-1, gc.getInfoTypeForString('DOMAIN_LAND')) < 2:
		return False
	if caster.baseCombatStr() < 1:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == false:
		iUnit = caster.getUnitType()
		if (iUnit != gc.getInfoTypeForString('UNIT_GALLEY') and iUnit != gc.getInfoTypeForString('UNIT_CARAVEL')):
			return false
	return True

def reqCrewNormalCrew(caster):
	pPlot = caster.plot()
	if (caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BUCCANEERS')) == False and caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SKELETON_CREW')) == False and caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LONGSHOREMEN')) == False):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		return False
	return True

def reqCrewSkeletonCrew(caster):
	pPlot = caster.plot()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SKELETON_CREW')):
		return False
	if caster.baseCombatStr() < 1:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == false:
		iUnit = caster.getUnitType()
		if (iUnit != gc.getInfoTypeForString('UNIT_QUEEN_OF_THE_LINE') and iUnit != gc.getInfoTypeForString('UNIT_TRIREME') and iUnit != gc.getInfoTypeForString('UNIT_GALLEON')):
			return false
	return True

def effectCrownOfBrillance(caster):
	caster.cast(gc.getInfoTypeForString('SPELL_CROWN_OF_BRILLANCE'))

def reqCrownOfBrillance(caster):
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CROWN_OF_BRILLANCE')):
		return False
	return True

def reqCrush(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot = CyMap().plot(iiX,iiY)
			bEnemy = false
			bNeutral = false
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if eTeam.isAtWar(pUnit.getTeam()):
					bEnemy = true
				else:
					bNeutral = true
			if (bEnemy and bNeutral == false):
				return true
	return false

def spellCrush(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iBestValue = 0
	pBestPlot = -1
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			bNeutral = false
			iValue = 0
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if eTeam.isAtWar(pUnit.getTeam()):
					iValue = iValue + 10
				else:
					bNeutral = true
			if (iValue > iBestValue and bNeutral == false):
				iBestValue = iValue
				pBestPlot = pPlot
	if pBestPlot != -1:
		for i in range(pBestPlot.getNumUnits()):
			pUnit = pBestPlot.getUnit(i)
			pUnit.doDamage(25, 75, caster, gc.getInfoTypeForString('DAMAGE_PHYSICAL'), true)
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_CRUSH'),pBestPlot.getPoint())

def reqDeclareNationality(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if (caster.getUnitAIType() in (UnitAITypes.UNITAI_PIRATE_SEA,UnitAITypes.UNITAI_ANIMAL)):
			return False
		if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN')) or caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_INVISIBLE')):
			return False
		if pPlayer.isBarbarian():
			return False
	return True

def reqDestroyUndead(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	eTeam = pPlayer.getTeam()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getRace() == gc.getInfoTypeForString('PROMOTION_UNDEAD'):
					if pPlayer.isHuman():
						return True
					p2Player = gc.getPlayer(pUnit.getOwner())
					e2Team = gc.getTeam(p2Player.getTeam())
					if e2Team.isAtWar(eTeam):
						return True
	return False

def spellDestroyUndead(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getRace() == gc.getInfoTypeForString('PROMOTION_UNDEAD'):
					pUnit.doDamage(30, 100, caster, gc.getInfoTypeForString('DAMAGE_HOLY'), true)

def reqDispelMagic(caster):
	if caster.canDispel(gc.getInfoTypeForString('SPELL_DISPEL_MAGIC')):
		return True
	pPlot = caster.plot()
	if pPlot.getBonusType(-1) != -1:
		if gc.getBonusInfo(pPlot.getBonusType(-1)).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_MANA'):
			if pPlot.getImprovementType() == -1:
				return True
			if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent() == False:
				return True
	return False

def spellDispelMagic(caster):
	pPlot = caster.plot()
	if pPlot.getBonusType(-1) != -1:
		if gc.getBonusInfo(pPlot.getBonusType(-1)).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_MANA'):
			if pPlot.getImprovementType() == -1:
				pPlot.setBonusType(gc.getInfoTypeForString('BONUS_MANA'))
			else:
				if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent() == False:
					pPlot.setBonusType(gc.getInfoTypeForString('BONUS_MANA'))
					pPlot.setImprovementType(-1)

def reqDisrupt(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if caster.getTeam() == pCity.getTeam():
		return False
	return True

def spellDisrupt(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iPlayer2 = pCity.getOwner()
	pPlayer2 = gc.getPlayer(iPlayer2)
	pCity.changeHurryAngerTimer(2)
	iRnd = CyGame().getSorenRandNum(3, "Disrupt")
	if iRnd != 0:
		pCity.changeCulture(iPlayer2,-1 * iRnd,True)
	CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISRUPT_ENEMY",()),'',1,'Art/Interface/Buttons/Spells/Disrupt.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
	CyInterface().addMessage(iPlayer2,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DISRUPT",()),'',1,'Art/Interface/Buttons/Spells/Disrupt.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	if pCity.getCulture(iPlayer2) < 1:
		pPlayer.acquireCity(pCity,false,false)
		pPlayer2.AI_changeAttitudeExtra(iPlayer,-4)

def reqDivineRetribution(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		eTeam = gc.getTeam(iTeam)
		if eTeam.getAtWarCount(True) < 2:
			return False
	return True

def spellDivineRetribution(caster):
	iDemon = gc.getInfoTypeForString('PROMOTION_DEMON')
	iUndead = gc.getInfoTypeForString('PROMOTION_UNDEAD')
	for iPlayer in range(gc.getMAX_PLAYERS()):
		player = gc.getPlayer(iPlayer)
		if player.isAlive():
			py = PyPlayer(iPlayer)
			for pUnit in py.getUnitList():
				if (pUnit.getRace() == iDemon or pUnit.getRace() == iUndead):
					pUnit.doDamage(50, 100, caster, gc.getInfoTypeForString('DAMAGE_HOLY'), false)

def reqDomination(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iResistMax = 95
	if pPlayer.isHuman() == false:
		iResistMax = 20
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.isAlive():
					if not pUnit.isDelayedDeath():
						if eTeam.isAtWar(pUnit.getTeam()):
							iResist = pUnit.getResistChance(caster, gc.getInfoTypeForString('SPELL_DOMINATION'))
							if iResist <= iResistMax:
								return true
	return false

def spellDomination(caster):
	iSpell = gc.getInfoTypeForString('SPELL_DOMINATION')
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iResistMax = 95
	iBestValue = 0
	pBestUnit = -1
	if pPlayer.isHuman() == false:
		iResistMax = 20
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				iValue = 0
				if pUnit.isAlive():
					if pUnit.isDelayedDeath() == False:
						if eTeam.isAtWar(pUnit.getTeam()):
							iResist = pUnit.getResistChance(caster, iSpell)
							if iResist <= iResistMax:
								iValue = pUnit.baseCombatStr() * 10
								iValue = iValue + (100 - iResist)
								if iValue > iBestValue:
									iBestValue = iValue
									pBestUnit = pUnit
	if pBestUnit != -1:
		pPlot = caster.plot()
		if pBestUnit.isResisted(caster, iSpell) == false:
			CyInterface().addMessage(pBestUnit.getOwner(),true,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOMINATION", ()),'',1,'Art/Interface/Buttons/Spells/Domination.dds',ColorTypes(7),pBestUnit.getX(),pBestUnit.getY(),True,True)
			CyInterface().addMessage(caster.getOwner(),true,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOMINATION_ENEMY", ()),'',1,'Art/Interface/Buttons/Spells/Domination.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			newUnit = pPlayer.initUnit(pBestUnit.getUnitType(), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			newUnit.convert(pBestUnit)
			newUnit.changeImmobileTimer(1)
		else:
			CyInterface().addMessage(caster.getOwner(),true,25,CyTranslator().getText("TXT_KEY_MESSAGE_DOMINATION_FAILED", ()),'',1,'Art/Interface/Buttons/Spells/Domination.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
			caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND3'), False)

def reqEarthquake(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		eTeam = pPlayer.getTeam()
		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				pPlot = CyMap().plot(iiX,iiY)
				p2Player = gc.getPlayer(pPlot.getOwner())
				if pPlot.isOwned():
					e2Team = gc.getTeam(p2Player.getTeam())
					if e2Team.isAtWar(eTeam) == False:
						return False
	return True

def spellEarthquake(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	eTeam = pPlayer.getTeam()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			if not pPlot.isNone():
				if (pPlot.isCity() or pPlot.getImprovementType() != -1):
					if pPlot.isOwned():
						cf.startWar(caster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_TOTAL)
				if pPlot.isCity():
					pCity = pPlot.getPlotCity()
					for i in range(gc.getNumBuildingInfos()):
						iRnd = CyGame().getSorenRandNum(100, "Bob")
						if (gc.getBuildingInfo(i).getConquestProbability() != 100 and iRnd <= 25):
							pCity.setNumRealBuilding(i, 0)
				for iUnit in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(iUnit)
					if pUnit.isFlying() == False:
						pUnit.setFortifyTurns(0)
				iRnd = CyGame().getSorenRandNum(100, "Bob")
				if iRnd <= 25:
					iImprovement = pPlot.getImprovementType()
					if iImprovement != -1:
						if gc.getImprovementInfo(iImprovement).isPermanent() == False:
							pPlot.setImprovementType(-1)

def spellEnterPortal(caster):
	pPlot = caster.plot()
	iX = pPlot.getPortalExitX()
	iY = pPlot.getPortalExitY()
	pExitPlot = CyMap().plot(iX,iY)
	if not pPlot.isNone():
		caster.setXY(iX, iY, false, true, true)

def spellEntertain(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	iPlayer2 = pCity.getOwner()
	if iPlayer != iPlayer2:
		pPlayer = gc.getPlayer(iPlayer)
		pPlayer2 = gc.getPlayer(iPlayer2)
		iGold = (pCity.getPopulation() / 2) + 1
		pPlayer.changeGold(iGold)
		szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_ENTERTAIN_GOOD", (iGold, ))
		CyInterface().addMessage(iPlayer,true,25,szBuffer,'',1,'Art/Interface/Buttons/Spells/Entertain.dds',ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
		iGold = iGold * -1
		pPlayer2.changeGold(iGold)
		szBuffer = CyTranslator().getText("TXT_KEY_MESSAGE_ENTERTAIN_BAD", (iGold, ))
		CyInterface().addMessage(iPlayer2,true,25,szBuffer,'',1,'Art/Interface/Buttons/Spells/Entertain.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
	pCity.changeHappinessTimer(2)

def reqEscape(caster):
	if caster.getOwner() == gc.getBARBARIAN_PLAYER():
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if caster.getDamage() >= 50:
			return False
	return True

def reqExploreLair(caster):
	if caster.isOnlyDefensive():
		return False
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
		return False
	if caster.isBarbarian():
		return False
	if caster.getDuration() > 0:
		return False
	if caster.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_SPELL'):
		return False
	if caster.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_BIRD'):
		return False
	pPlot = caster.plot()
	if not pPlot.isWater():
		pPlayer = gc.getPlayer(caster.getOwner())
		iTeam = pPlayer.getTeam()
		eTeam = gc.getTeam(iTeam)
		bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
		if not eTeam.isAtWar(bPlayer.getTeam()):
			return False
	return True

def spellExploreLair(caster):
	pPlot = caster.plot()
	iRnd = CyGame().getSorenRandNum(100, "Explore Lair") + caster.getLevel() + caster.baseCombatStr()
	iDestroyLair = 0
	if iRnd < 14:
		iDestroyLair = cf.exploreLairBigBad(caster)
	if iRnd >= 14 and iRnd < 44:
		iDestroyLair = cf.exploreLairBad(caster)
	if iRnd >= 44 and iRnd < 74:
		iDestroyLair = cf.exploreLairNeutral(caster)
	if iRnd >= 74 and iRnd < 94:
		iDestroyLair = cf.exploreLairGood(caster)
	if iRnd >= 94:
		iDestroyLair = cf.exploreLairBigGood(caster)
	if iDestroyLair > CyGame().getSorenRandNum(100, "Explore Lair"):
		CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_LAIR_DESTROYED", ()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		pPlot.setImprovementType(-1)
	caster.finishMoves()

	caster.changeExperience(1, -1, false, false, false)

def spellExploreLairEpic(caster):
	pPlot = caster.plot()
	iRnd = CyGame().getSorenRandNum(100, "Explore Lair") + caster.getLevel() + caster.baseCombatStr()
	iDestroyLair = 0
	if iRnd < 54:
		iDestroyLair = cf.exploreLairBigBad(caster)
	if iRnd >= 54:
		iDestroyLair = cf.exploreLairBigGood(caster)
	if iDestroyLair > CyGame().getSorenRandNum(100, "Explore Lair"):
		CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_LAIR_DESTROYED", ()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Spells/Explore Lair.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		pPlot.setImprovementType(-1)
	caster.finishMoves()
	caster.changeExperience(1, -1, false, false, false)

def reqFeast(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if pCity.getPopulation() < 3:
		return False
	return True

def spellFeast(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	caster.changeExperience(pCity.getPopulation()/2, -1, false, false, false)
	pCity.changePopulation(-1)
	pCity.changeHurryAngerTimer(3)

def reqFeed(caster):
	if caster.getDamage() == 0:
		return false
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == false:
		if caster.getDamage() < 20:
			return false
	return true

def spellFeed(caster):
	caster.setDamage(caster.getDamage() - 20, caster.getOwner())
	pVictim = -1
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == caster.getOwner():
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_BLOODPET'):
				if (pVictim == -1 or pVictim.getLevel() > pUnit.getLevel()):
					pVictim = pUnit
	if pVictim != -1:
		pVictim.kill(True, 0)

def reqForTheHorde(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	eTeam = gc.getTeam(pPlayer.getTeam())
	if eTeam.isAtWar(bPlayer.getTeam()):
		return False
	if bPlayer.getNumUnits() == 0:
		return False
	if pPlayer.isHuman() == False:
		if bPlayer.getNumUnits() < 60:
			return False
	return True

def spellForTheHorde(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHero = gc.getInfoTypeForString('PROMOTION_HERO')
	iOrc = gc.getInfoTypeForString('PROMOTION_ORC')
	py = PyPlayer(gc.getBARBARIAN_PLAYER())
	for pUnit in py.getUnitList():
		if (pUnit.getRace() == iOrc and pUnit.isHasPromotion(iHero) == False):
			if CyGame().getSorenRandNum(100, "Bob") < 50:
				pPlot = pUnit.plot()
				for i in range(pPlot.getNumUnits(), -1, -1):
					pNewPlot = -1
					pLoopUnit = pPlot.getUnit(i)
					if pLoopUnit.isHiddenNationality():
						pNewPlot = cf.findClearPlot(pLoopUnit, -1)
						if pNewPlot != -1:
							pLoopUnit.setXY(pNewPlot.getX(), pNewPlot.getY(), false, true, true)
				newUnit = pPlayer.initUnit(pUnit.getUnitType(), pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit.convert(pUnit)

def reqFormWolfPack(caster):
	pPlot = caster.plot()
	iWolf = gc.getInfoTypeForString('UNIT_WOLF')
	iCount = 0
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == iWolf:
			if pUnit.getOwner() == caster.getOwner():
				iCount += 1
	if iCount < 2:
		return False
	return True

def spellFormWolfPack(caster):
	pPlot = caster.plot()
	iWolf = gc.getInfoTypeForString('UNIT_WOLF')
	pWolf2 = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getUnitType() == iWolf:
			if pUnit.getOwner() == caster.getOwner():
				if pUnit.getID() != caster.getID():
					pWolf2 = pUnit
	if pWolf2 != -1:
		pPlayer = gc.getPlayer(caster.getOwner())
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOLF_PACK'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.setExperience(caster.getExperience() + pWolf2.getExperience(), -1)
		caster.kill(True, 0)
		pWolf2.kill(True, 0)

def reqGiftsOfNantosuelta(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() == 0:
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellGiftsOfNantosuelta(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iGoldenHammer = gc.getInfoTypeForString('EQUIPMENT_GOLDEN_HAMMER')
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		newUnit = pPlayer.initUnit(iGoldenHammer, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqGiftVampirism(caster):
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE')):
				if pUnit.getLevel() >= 6:
					return True
				if (pUnit.getLevel() >= 4 and pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_MOROI')):
					return True
	return False

def spellGiftVampirism(caster):
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE')):
				if pUnit.getLevel() >= 6:
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE'),True)
				if (pUnit.getLevel() >= 4 and pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_MOROI')):
					pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_VAMPIRE'),True)

def spellGiveHammerToCraftsman(caster):
	pCity = caster.plot().getPlotCity()
	pCity.changeFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_ENGINEER'), 1)

def reqHastursRazor(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	eTeam = pPlayer.getTeam()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getDamage() > 0:
					if pPlayer.isHuman():
						return True
					if pUnit.getOwner() == caster.getOwner():
						return True
	return False

def spellHastursRazor(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	listDamage = []
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				listDamage.append(pUnit.getDamage())
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				iRnd = listDamage[CyGame().getSorenRandNum(len(listDamage), "Hasturs Razor")]
				if iRnd != pUnit.getDamage():
					CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_HASTURS_RAZOR",()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Spells/Hasturs Razor.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
					if pUnit.getOwner() != caster.getOwner():
						CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_HASTURS_RAZOR",()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Spells/Hasturs Razor.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
					pUnit.setDamage(iRnd, caster.getOwner())

def reqHeal(caster):
	pPlot = caster.plot()
	iPoisoned = gc.getInfoTypeForString('PROMOTION_POISONED')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getDamage() > 0):
			return True
		if pUnit.isHasPromotion(iPoisoned):
			return True
	return False

def spellHeal(caster,amount):
	pPlot = caster.plot()
	iPoisoned = gc.getInfoTypeForString('PROMOTION_POISONED')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		pUnit.setHasPromotion(iPoisoned,False)
		if pUnit.isAlive():
			pUnit.changeDamage(-amount,0) #player doesn't matter - it won't kill

def reqHealingSalve(caster):
	if caster.getDamage() == 0:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if caster.getDamage() < 25:
			return False
	return True

def spellHealingSalve(caster):
	caster.setDamage(0, caster.getOwner())
	caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DISEASED'), false)
	caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED'), false)
	caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED'), false)
	caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WITHERED'), false)
	
def reqHellfire(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
		return False
	pPlot = caster.plot()
	if pPlot.isCity():
		return False
	if pPlot.isWater():
		return False
	if pPlot.getImprovementType() != -1:
		return False
	iHellFire = gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')
	iX = pPlot.getX()
	iY = pPlot.getY()
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if pPlot2.getImprovementType() == iHellFire:
				return False
	if pPlayer.isHuman() == False:
		if pPlot.isOwned():
			if pPlot.getOwner() == caster.getOwner():
				return False
	return True

def reqHeraldsCall(caster):
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			return true
	return False

def spellHeraldsCall(caster):
	iValor = gc.getInfoTypeForString('PROMOTION_VALOR')
	iBlessed = gc.getInfoTypeForString('PROMOTION_BLESSED')
	iCourage = gc.getInfoTypeForString('PROMOTION_COURAGE')
	iLoyalty = gc.getInfoTypeForString('PROMOTION_LOYALTY')
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.isAlive() and pUnit.getOwner() == caster.getOwner()):
			pUnit.setHasPromotion(iValor,True)
			pUnit.setHasPromotion(iBlessed, True)
			pUnit.setHasPromotion(iCourage, True)
			pUnit.setHasPromotion(iLoyalty, True)
			pUnit.setDuration(1)

def reqHide(caster):
	if caster.isMadeAttack():
		return False
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN')):
		return False
	return True

def reqHireScorpionClan(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
	eTeam = gc.getTeam(pPlayer.getTeam())
	if eTeam.isAtWar(bPlayer.getTeam()):
		return False
	return True

def spellHireArcher(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.initUnit(gc.getInfoTypeForString('UNIT_ARCHER_SCORPION_CLAN'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellHireChariot(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.initUnit(gc.getInfoTypeForString('UNIT_CHARIOT_SCORPION_CLAN'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellHireGoblin(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.initUnit(gc.getInfoTypeForString('UNIT_GOBLIN_SCORPION_CLAN'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellHireUnits(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pCity = caster.plot().getPlotCity()
	iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_MAGNADINE_HIRE_UNITS')
	triggerData = pPlayer.initTriggeredData(iEvent, true, pCity.getID(), pCity.getX(), pCity.getY(), iPlayer, -1, -1, -1, -1, -1)

def spellHireWolfRider(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.initUnit(gc.getInfoTypeForString('UNIT_WOLF_RIDER_SCORPION_CLAN'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqHyboremsWhisper(caster):
	if gc.getGame().isNetworkMultiPlayer():
		return False
	pCity = cf.getAshenVeilCity(3)
	if pCity == -1:
		return False
	return True

def spellHyboremsWhisper(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_HYBOREMS_WHISPER')
	triggerData = pPlayer.initTriggeredData(iEvent, true, -1, caster.getX(), caster.getY(), iPlayer, -1, -1, -1, -1, -1)

def reqImpersonateLeader(caster):
	pCity = caster.plot().getPlotCity()
	if pCity.getOwner() == caster.getOwner():
		return False
	if gc.getPlayer(pCity.getOwner()).isHuman():
		return False
	return True

def spellImpersonateLeader(caster):
	pCity = caster.plot().getPlotCity()
	iNewPlayer = pCity.getOwner()
	iOldPlayer = caster.getOwner()
	iTimer = 5 + CyGame().getSorenRandNum(10, "Impersonate Leader")
	CyGame().reassignPlayerAdvanced(iOldPlayer, iNewPlayer, iTimer)

def reqInquisition(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	StateBelief = pPlayer.getStateReligion()
	if StateBelief == -1:
		if caster.getOwner() != pCity.getOwner():
			return False
	if (StateBelief != gc.getPlayer(pCity.getOwner()).getStateReligion()):
		return False
	for iTarget in range(gc.getNumReligionInfos()):
		if (StateBelief != iTarget and pCity.isHasReligion(iTarget) and pCity.isHolyCityByType(iTarget) == False):
			return True
	return False

def spellInquisition(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	StateBelief = gc.getPlayer(pCity.getOwner()).getStateReligion()
	iRnd = CyGame().getSorenRandNum(4, "Bob")
	if StateBelief == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
		iRnd = iRnd - 1
	for iTarget in range(gc.getNumReligionInfos()):
		if (not StateBelief == iTarget and pCity.isHasReligion(iTarget) and not pCity.isHolyCityByType(iTarget)):
			pCity.setHasReligion(iTarget, False, True, True)
			iRnd = iRnd + 1
			for i in range(gc.getNumBuildingInfos()):
				if gc.getBuildingInfo(i).getPrereqReligion() == iTarget:
					pCity.setNumRealBuilding(i, 0)
	if iRnd >= 1:
		pCity.changeHurryAngerTimer(iRnd)

def reqIntoTheMist(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getNumUnits() < 40:
			return False
	return True

def spellIntoTheMist(caster):
	iInvisible = gc.getInfoTypeForString('PROMOTION_HIDDEN')
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		pUnit.setHasPromotion(iInvisible, True)

def reqIraUnleashed(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_IRA')) >= 4:
		return False
	return True

def spellIraUnleashed(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iCount = 4 - pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_IRA'))
	for i in range(iCount):
		pPlayer.initUnit(gc.getInfoTypeForString('UNIT_IRA'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqKidnap(caster):
	pCity = caster.plot().getPlotCity()
	if pCity.getTeam() == caster.getTeam():
		return False
	i = 0
	i = i + pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_PRIEST'))
	i = i + pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_ARTIST'))
	i = i + pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_MERCHANT'))
	i = i + pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_ENGINEER'))
	i = i + pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_SCIENTIST'))
	if i == 0:
		return False
	return True

def spellKidnap(caster):
	pCity = caster.plot().getPlotCity()
	if pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_PRIEST')) > 0:
		iUnit = gc.getInfoTypeForString('UNIT_PROPHET')
		iSpec = gc.getInfoTypeForString('SPECIALIST_GREAT_PRIEST')
	if pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_ARTIST')) > 0:
		iUnit = gc.getInfoTypeForString('UNIT_ARTIST')
		iSpec = gc.getInfoTypeForString('SPECIALIST_GREAT_ARTIST')
	if pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_MERCHANT')) > 0:
		iUnit = gc.getInfoTypeForString('UNIT_MERCHANT')
		iSpec = gc.getInfoTypeForString('SPECIALIST_GREAT_MERCHANT')
	if pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_ENGINEER')) > 0:
		iUnit = gc.getInfoTypeForString('UNIT_ENGINEER')
		iSpec = gc.getInfoTypeForString('SPECIALIST_GREAT_ENGINEER')
	if pCity.getFreeSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_SCIENTIST')) > 0:
		iUnit = gc.getInfoTypeForString('UNIT_SCIENTIST')
		iSpec = gc.getInfoTypeForString('SPECIALIST_GREAT_SCIENTIST')
	iChance = caster.baseCombatStr() * 8
	if iChance > 95:
		iChance = 95
	pPlayer = gc.getPlayer(caster.getOwner())
	if CyGame().getSorenRandNum(100, "Kidnap") <= iChance:
		newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		pCity.changeFreeSpecialistCount(iSpec, -1)
	else:
		if CyGame().getSorenRandNum(100, "Kidnap") <= 50:
			caster.setXY(pPlayer.getCapitalCity().getX(), pPlayer.getCapitalCity().getY(), false, true, true)
		else:
			caster.kill(True, 0)
		cf.startWar(caster.getOwner(), pCity.getOwner(), WarPlanTypes.WARPLAN_TOTAL)

def reqLegends(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() == 0:
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellLegends(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		pCity.changeCulture(iPlayer, 300, True)

def reqLichdom(caster):
	if caster.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_FLESH_GOLEM'):
		return False
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PUPPET')):
		return False
	if isWorldUnitClass(caster.getUnitClassType()):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LICH')) >= 4:
		return False
	return True

def reqMask(caster):
	if caster.isHiddenNationality():
		return False
	if caster.hasCargo():
		return False
	if caster.isCargo():
		return False
	pGroup = caster.getGroup()
	if pGroup.isNone() == False:
		if pGroup.getNumUnits() > 1:
			return False
	return True

def reqMezmerizeAnimal(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'):
					if eTeam.isAtWar(pUnit.getTeam()):
						return True
	return False

def spellMezmerizeAnimal(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'):
					if eTeam.isAtWar(pUnit.getTeam()):
						if pUnit.isDelayedDeath() == False:
							if pUnit.isResisted(caster, gc.getInfoTypeForString('SPELL_MEZMERIZE_ANIMAL')) == False:
								newUnit = pPlayer.initUnit(pUnit.getUnitType(), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
								newUnit.convert(pUnit)

def reqMirror(caster):
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	if caster.isImmuneToMagic():
		return False
	if pPlot.isVisibleEnemyUnit(iPlayer):
		return False
	return True

def spellMirror(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	newUnit = pPlayer.initUnit(caster.getUnitType(), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	for i in range(gc.getNumPromotionInfos()):
		newUnit.setHasPromotion(i, caster.isHasPromotion(i))
		if gc.getPromotionInfo(i).isEquipment():
			newUnit.setHasPromotion(i, False)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION'), True)
	newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_IMMORTAL'), False)
	if newUnit.isImmortal():
		newUnit.changeImmortal(-1)
	newUnit.setDamage(caster.getDamage(), caster.getOwner())
	newUnit.setLevel(caster.getLevel())
	newUnit.setExperience(caster.getExperience(), -1)
	newUnit.setHasCasted(True)
	newUnit.setDuration(1)

def reqPeace(caster):
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_CHANGING_WAR_PEACE):
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	if eTeam.getAtWarCount(True) == 0:
		return False
	return True

def spellPeace(caster):
	eTeam = gc.getTeam(gc.getPlayer(caster.getOwner()).getTeam())
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isAlive() and iPlayer != caster.getOwner() and iPlayer != gc.getBARBARIAN_PLAYER()):
			i2Team = gc.getPlayer(iPlayer).getTeam()
			if eTeam.isAtWar(i2Team):
				eTeam.makePeace(i2Team)
	CyGame().changeGlobalCounter(-1 * (CyGame().getGlobalCounter() / 2))

def reqPeaceSevenPines(caster):
	pPlot = caster.plot()
	if not pPlot.isPythonActive():
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	if eTeam.getAtWarCount(True) == 0:
		return False
	return True

def spellPeaceSevenPines(caster):
	eTeam = gc.getTeam(gc.getPlayer(caster.getOwner()).getTeam())
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isAlive() and iPlayer != caster.getOwner() and iPlayer != gc.getBARBARIAN_PLAYER()):
			i2Team = gc.getPlayer(iPlayer).getTeam()
			if eTeam.isAtWar(i2Team):
				eTeam.makePeace(i2Team)
	CyGame().changeGlobalCounter(-1 * (CyGame().getGlobalCounter() / 2))
	pPlot = caster.plot()
	pPlot.setPythonActive(False)

def reqPillarofFire(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot = CyMap().plot(iiX,iiY)
			bEnemy = false
			bNeutral = false
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if eTeam.isAtWar(pUnit.getTeam()):
					bEnemy = true
				else:
					bNeutral = true
			if (bEnemy and bNeutral == false):
				return true
	return false

def spellPillarofFire(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	iBestValue = 0
	pBestPlot = -1
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			bNeutral = false
			iValue = 0
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if eTeam.isAtWar(pUnit.getTeam()):
					iValue += 5 * pUnit.baseCombatStr()
				else:
					bNeutral = true
			if (iValue > iBestValue and bNeutral == false):
				iBestValue = iValue
				pBestPlot = pPlot
	if pBestPlot != -1:
		for i in range(pBestPlot.getNumUnits()):
			pUnit = pBestPlot.getUnit(i)
			pUnit.doDamage(25, 75, caster, gc.getInfoTypeForString('DAMAGE_FIRE'), true)
		if (pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FOREST') or pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_JUNGLE')):
			bValid = True
			iImprovement = pPlot.getImprovementType()
			if iImprovement != -1 :
				if gc.getImprovementInfo(iImprovement).isPermanent():
					bValid = False
			if bValid:
				if CyGame().getSorenRandNum(100, "Flames Spread") <= gc.getDefineINT('FLAMES_SPREAD_CHANCE'):
					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_SMOKE'))
		CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_PILLAR_OF_FIRE'),pBestPlot.getPoint())

def reqPirateCove(caster):
	pPlot = caster.plot()
	iPirateCove = gc.getInfoTypeForString('IMPROVEMENT_PIRATE_COVE')
	if pPlot.getOwner() != caster.getOwner():
		return False
	if pPlot.canHaveImprovement(iPirateCove, -1, False) == False:
		return False
	if pPlot.getImprovementType() != -1:
		return False
	if pPlot.getBonusType(-1) != -1:
		return False
	iPirateHarbor = gc.getInfoTypeForString('IMPROVEMENT_PIRATE_HARBOR')
	iPiratePort = gc.getInfoTypeForString('IMPROVEMENT_PIRATE_PORT')
	iX = caster.getX()
	iY = caster.getY()
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot = CyMap().plot(iiX,iiY)
			if not pPlot.isNone():
				iImprovement = pPlot.getImprovementType()
				if iImprovement == iPirateCove:
					return False
				if iImprovement == iPirateHarbor:
					return False
				if iImprovement == iPiratePort:
					return False
	return True

def reqMarchOfTheTrees(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		eTeam = gc.getTeam(iTeam)
		if eTeam.getAtWarCount(True) < 2:
			return False
	return True

def spellMarchOfTheTrees(caster):
	iAncientForest = gc.getInfoTypeForString('FEATURE_FOREST_ANCIENT')
	iForest = gc.getInfoTypeForString('FEATURE_FOREST')
	iNewForest = gc.getInfoTypeForString('FEATURE_FOREST_NEW')
	iTreant = gc.getInfoTypeForString('UNIT_TREANT')
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				if (pPlot.getFeatureType() == iForest or pPlot.getFeatureType() == iAncientForest):
					if not pPlot.isVisibleEnemyUnit(iPlayer):
						newUnit = pPlayer.initUnit(iTreant, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
						newUnit.setDuration(5)
						pPlot.setFeatureType(iNewForest,0)

def reqMotherLode(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MINE')) < 10:
			return False
	return True

def spellMotherLode(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.changeGold(pPlayer.getImprovementCount(gc.getInfoTypeForString('IMPROVEMENT_MINE')) * 25)
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				if pPlot.isWater() == False:
					if pPlot.isPeak() == False:
						if pPlot.isHills() == False:
							if CyGame().getSorenRandNum(100, "Mother Lode") < 10:
								pPlot.setPlotType(PlotTypes.PLOT_HILLS, True, True)

def spellOpenChest(caster):
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	bValid = True
	if CyGame().getWBMapScript():
		bValid = sf.openChest(caster, pPlot)
	if bValid:
		if CyGame().getSorenRandNum(100, "Explore Lair") < 25:
			lTrapList = ['POISON', 'FIRE', 'SPORES']
			sTrap = lTrapList[CyGame().getSorenRandNum(len(lTrapList), "Pick Trap")-1]
			point = pPlot.getPoint()
			if sTrap == 'POISON':
				caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED'), True)
				caster.doDamageNoCaster(25, 90, gc.getInfoTypeForString('DAMAGE_POISON'), false)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TRAP_POISON", ()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Promotions/Poisoned.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			if sTrap == 'FIRE':
				caster.doDamageNoCaster(50, 90, gc.getInfoTypeForString('DAMAGE_FIRE'), false)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TRAP_FIRE", ()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Spells/Ring of Flames.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
				CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_RING_OF_FLAMES'),point)
				CyAudioGame().Play3DSound("AS3D_SPELL_FIREBALL",point.x,point.y,point.z)
			if sTrap == 'SPORES':
				caster.changeImmobileTimer(3)
				CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TRAP_SPORES", ()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Spells/Spores.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
				CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPORES'),point)
				CyAudioGame().Play3DSound("AS3D_SPELL_CONTAGION",point.x,point.y,point.z)

		lList = ['EMPTY', 'HIGH_GOLD', 'ITEM_HEALING_SALVE', 'ITEM_JADE_TORC', 'ITEM_ROD_OF_WINDS', 'ITEM_TIMOR_MASK', 'TECH']
		sGoody = lList[CyGame().getSorenRandNum(len(lList), "Pick Goody")-1]
		if sGoody == 'EMPTY':
			CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_EXPLORE_LAIR_TREASURE_EMPTY",()),'AS2D_POSITIVE_DINK',1,'Art/Interface/Buttons/Equipment/Treasure.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		if sGoody == 'HIGH_GOLD':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_HIGH_GOLD'), caster)
		if sGoody == 'ITEM_HEALING_SALVE':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_HEALING_SALVE'), caster)
		if sGoody == 'ITEM_JADE_TORC':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_JADE_TORC'), caster)
		if sGoody == 'ITEM_POTION_OF_INVISIBILITY':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_INVISIBILITY'), caster)
		if sGoody == 'ITEM_POTION_OF_RESTORATION':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_POTION_OF_RESTORATION'), caster)
		if sGoody == 'ITEM_ROD_OF_WINDS':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_ROD_OF_WINDS'), caster)
		if sGoody == 'ITEM_TIMOR_MASK':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_EXPLORE_LAIR_ITEM_TIMOR_MASK'), caster)
		if sGoody == 'TECH':
			pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_TECH'), caster)
		pTreasure = -1
		iTreasure = gc.getInfoTypeForString('EQUIPMENT_TREASURE')
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getUnitType() == iTreasure:
				pTreasure = pUnit
		pTreasure.kill(True, 0)

def reqPromoteSettlement(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	if not pCity.isSettlement():
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() - pPlayer.getNumSettlements() >= pPlayer.getMaxCities():
		return False
	return True

def spellPromoteSettlement(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCity.setSettlement(False)
	pCity.setPlotRadius(3)

def reqRagingSeas(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		eTeam = gc.getTeam(pPlayer.getTeam())
		iArcane = gc.getInfoTypeForString('UNITCLASS_ARCANE_BARGE')
		iCaravel = gc.getInfoTypeForString('UNITCLASS_CARAVEL')
		iGalley = gc.getInfoTypeForString('UNITCLASS_GALLEY')
		iFrigate = gc.getInfoTypeForString('UNITCLASS_FRIGATE')
		iGalleon = gc.getInfoTypeForString('UNITCLASS_GALLEON')
		iManOWar = gc.getInfoTypeForString('UNITCLASS_MAN_O_WAR')
		iPrivateer = gc.getInfoTypeForString('UNITCLASS_PRIVATEER')
		iQueenOfTheLine = gc.getInfoTypeForString('UNITCLASS_QUEEN_OF_THE_LINE')
		iTrireme = gc.getInfoTypeForString('UNITCLASS_TRIREME')
		for iPlayer2 in range(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if pPlayer2.isAlive():
				iTeam2 = gc.getPlayer(iPlayer2).getTeam()
				if eTeam.isAtWar(iTeam2):
					iCount = pPlayer2.getUnitClassCount(iArcane)
					iCount += pPlayer2.getUnitClassCount(iCaravel)
					iCount += pPlayer2.getUnitClassCount(iGalley)
					iCount += pPlayer2.getUnitClassCount(iFrigate) * 2
					iCount += pPlayer2.getUnitClassCount(iGalleon) * 2
					iCount += pPlayer2.getUnitClassCount(iManOWar) * 3
					iCount += pPlayer2.getUnitClassCount(iPrivateer)
					iCount += pPlayer2.getUnitClassCount(iQueenOfTheLine) * 3
					iCount += pPlayer2.getUnitClassCount(iTrireme)
					if iCount > 10:
						return True
		return False
	return True

def spellRagingSeas(caster):
	iCold = gc.getInfoTypeForString('DAMAGE_COLD')
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iLanun = gc.getInfoTypeForString('CIVILIZATION_LANUN')
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iSpring = gc.getInfoTypeForString('EFFECT_SPRING')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isAdjacentToWater():
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if pUnit.getCivilizationType() != iLanun:
					pUnit.doDamageNoCaster(75, 100, iCold, false)
			if pPlot.getImprovementType() != -1:
				if pPlot.getFeatureType() == iFlames:
					pPlot.setFeatureType(-1, 0)
				if pPlot.getImprovementType() == iSmoke:
					pPlot.setImprovementType(-1)
				else:
					if pPlot.isOwned():
						if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent() == False:
							if gc.getPlayer(pPlot.getOwner()).getCivilizationType() != iLanun:
								if CyGame().getSorenRandNum(100, "Raging Seas") <= 25:
									pPlot.setImprovementType(-1)
			if pPlot.isVisibleToWatchingHuman():
				CyEngine().triggerEffect(iSpring,pPlot.getPoint())

def spellRaiseSkeleton(caster):
	pPlot = caster.plot()
	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD'):
		pPlot.setImprovementType(-1)
		caster.cast(gc.getInfoTypeForString('SPELL_RAISE_SKELETON'))
		caster.cast(gc.getInfoTypeForString('SPELL_RAISE_SKELETON'))

def reqRally(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) != gc.getInfoTypeForString('CIVIC_CRUSADE'):
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellRally(caster):
	iOwner = caster.getOwner()
	pPlayer = gc.getPlayer(iOwner)
	iDemagog = gc.getInfoTypeForString('UNIT_DEMAGOG')
	iTown = gc.getInfoTypeForString('IMPROVEMENT_TOWN')
	iVillage = gc.getInfoTypeForString('IMPROVEMENT_VILLAGE')
	iCount = 0
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.getOwner() == iOwner:
			if not pPlot.isVisibleEnemyUnit(iOwner):
				if pPlot.isCity():
					newUnit = pPlayer.initUnit(iDemagog, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				if pPlot.getImprovementType() == iTown:
					pPlot.setImprovementType(iVillage)
					newUnit = pPlayer.initUnit(iDemagog, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def spellReadTheGrimoire(caster):
	iRnd = CyGame().getSorenRandNum(100, "Read the Grimoire")
	if iRnd < 20:
		caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_SPECTRE'))
	if iRnd >= 20 and iRnd < 40:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_UNHOLY_TAINT'), True)
	if iRnd >= 40 and iRnd < 60:
		caster.cast(gc.getInfoTypeForString('SPELL_WITHER'))
	if iRnd >= 60 and iRnd < 70:
		caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_PIT_BEAST'))
	if iRnd >= 70 and iRnd < 80:
		caster.cast(gc.getInfoTypeForString('SPELL_BURNING_BLOOD'))
	if iRnd >= 80 and iRnd < 90:
		caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DEMON'), True)
	if iRnd >= 90:
		caster.kill(True, PlayerTypes.NO_PLAYER)

def reqRebuildBarnaxus(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	if caster.getUnitType() == gc.getInfoTypeForString('UNIT_BARNAXUS'):
		return False
	if pCityPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
		return False
	return True

def spellRebuildBarnaxus(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	pCityPlayer = gc.getPlayer(pCity.getOwner())
	newUnit = pCityPlayer.initUnit(gc.getInfoTypeForString('UNIT_BARNAXUS'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.setDamage(75, caster.getOwner())
	newUnit.finishMoves()
	pCity.applyBuildEffects(newUnit)
	if pPlayer.getCivilizationType() != gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
		pCityPlayer.AI_changeAttitudeExtra(iPlayer,2)

def spellRecruit(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	eTeam = gc.getTeam(pPlayer.getTeam())
	iLoop = (pCity.getPopulation() / 3) + 1
	if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')) == 1:
		iLoop = iLoop * 2
	for i in range(iLoop):
		iRnd = CyGame().getSorenRandNum(60, "Bob")
		iUnit = -1
		if iRnd <= 10:
			iUnit = gc.getInfoTypeForString('UNITCLASS_SCOUT')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_HUNTER')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HANDLING')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_RANGER')
		elif iRnd <= 20:
			iUnit = gc.getInfoTypeForString('UNITCLASS_SCOUT')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_HUNTER')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_POISONS')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_ASSASSIN')
		elif iRnd <= 30:
			iUnit = gc.getInfoTypeForString('UNITCLASS_SCOUT')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_HORSEMAN')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_STIRRUPS')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER')
		elif iRnd <= 40:
			iUnit = gc.getInfoTypeForString('UNITCLASS_SCOUT')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_HORSEMAN')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_TRADE')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_CHARIOT')
		elif iRnd <= 50:
			iUnit = gc.getInfoTypeForString('UNITCLASS_WARRIOR')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_AXEMAN')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_CHAMPION')
		elif iRnd <= 60:
			iUnit = gc.getInfoTypeForString('UNITCLASS_WARRIOR')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ARCHERY')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_ARCHER')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BOWYERS')):
				iUnit = gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN')
		if iUnit != -1:
			infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
			iUnit = infoCiv.getCivilizationUnits(iUnit)
			if iUnit != -1:
				newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	caster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_RECRUITER'), False)
	if caster.getUnitType() != gc.getInfoTypeForString('UNIT_DONAL'):
		caster.kill(True, PlayerTypes.NO_PLAYER)

def reqRecruitMercenary(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		pPlot = caster.plot()
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
			return False
		iX = caster.getX()
		iY = caster.getY()
		eTeam = gc.getTeam(pPlayer.getTeam())
		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				pPlot = CyMap().plot(iiX,iiY)
				for i in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					p2Player = gc.getPlayer(pUnit.getOwner())
					e2Team = p2Player.getTeam()
					if eTeam.isAtWar(e2Team) == True:
						return True
		return False
	return True

def spellRecruitMercenary(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iUnit = gc.getInfoTypeForString('UNITCLASS_MERCENARY')
	infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit = infoCiv.getCivilizationUnits(iUnit)
	newUnit = pPlayer.initUnit(iUnit, caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	newUnit.finishMoves()
	newUnit.setHasCasted(True)
	if caster.getUnitType() == gc.getInfoTypeForString('UNIT_MAGNADINE'):
		newUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_LOYALTY'), True)

def spellReleaseFromCage(caster):
	pPlot = caster.plot()
	pPlot.setImprovementType(-1)

def reqReligiousFervor(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iReligion = pPlayer.getStateReligion()
	if iReligion == -1:
		return False
	if pPlayer.isHuman() == False:
		iCount = 0
		for pyCity in PyPlayer(iPlayer).getCityList() :
			pCity = pyCity.GetCy()
			if pCity.isHasReligion(iReligion):
				iCount += 1
		if iCount < 5:
			return False
	return True

def spellReligiousFervor(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	iReligion = pPlayer.getStateReligion()
	if iReligion == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
		iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES')
	if iReligion == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
		iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_KILMORPH')
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
		iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_EMPYREAN')
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
		iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER')
	if iReligion == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
		iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_OVERLORDS')
	if iReligion == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
		iUnit = gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_VEIL')
	if iReligion == gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
		iUnit = gc.getInfoTypeForString('UNIT_ASSASSIN')
	iCount = 0
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		if pCity.isHasReligion(iReligion):
			iCount += 1
	for pyCity in PyPlayer(iPlayer).getCityList() :
		pCity = pyCity.GetCy()
		newUnit = pPlayer.initUnit(iUnit, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
		newUnit.changeExperience(iCount, -1, False, False, False)
		newUnit.setReligion(iReligion)

def reqRepair(caster):
	pPlot = caster.plot()
	iGolem = gc.getInfoTypeForString('PROMOTION_GOLEM')
	iNaval = gc.getInfoTypeForString('UNITCOMBAT_NAVAL')
	iSiege = gc.getInfoTypeForString('UNITCOMBAT_SIEGE')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getUnitCombatType() == iSiege or pUnit.getUnitCombatType() == iNaval or pUnit.isHasPromotion(iGolem)):
			if pUnit.getDamage() > 0:
				return True
	return False

def spellRepair(caster,amount):
	pPlot = caster.plot()
	iGolem = gc.getInfoTypeForString('PROMOTION_GOLEM')
	iNaval = gc.getInfoTypeForString('UNITCOMBAT_NAVAL')
	iSiege = gc.getInfoTypeForString('UNITCOMBAT_SIEGE')
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getUnitCombatType() == iSiege or pUnit.getUnitCombatType() == iNaval or pUnit.isHasPromotion(iGolem)):
			pUnit.changeDamage(-amount,0)

def reqRessurection(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iHero = cf.getHero(pPlayer)
	if iHero == -1:
		return False
	if not CyGame().isUnitClassMaxedOut(iHero, 0):
		return False
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.getUnitClassCount(iHero) > 0:
			return False
	py = PyPlayer(caster.getOwner())
	iSpell = gc.getInfoTypeForString('SPELL_RESSURECTION')
	for pUnit in py.getUnitList():
		if pUnit.getDelayedSpell() == iSpell:
			return False
	return True

def spellRessurection(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	iHero = cf.getHero(pPlayer)
	infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit = infoCiv.getCivilizationUnits(iHero)
	iBarn = gc.getInfoTypeForString('EQUIPMENT_PIECES_OF_BARNAXUS')
	iBarnProm = gc.getInfoTypeForString('PROMOTION_PIECES_OF_BARNAXUS')
	if iUnit == gc.getInfoTypeForString('UNIT_BARNAXUS'):
		for iPlayer2 in range(gc.getMAX_PLAYERS()):
			pPlayer2 = gc.getPlayer(iPlayer2)
			if pPlayer2.isAlive():
				py = PyPlayer(iPlayer2)
				for pUnit in py.getUnitList():
					if pUnit.isHasPromotion(iBarnProm):
						pUnit.setHasPromotion(iBarnProm, False)
						CyInterface().addMessage(iPlayer2,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PIECES_LOST", ()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Units/Barnaxus.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
					if pUnit.getUnitType() == iBarn:
						CyInterface().addMessage(iPlayer2,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PIECES_LOST", ()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Units/Barnaxus.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)
						pUnit.kill(True, PlayerTypes.NO_PLAYER)
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
	for iProm in range(gc.getNumPromotionInfos()):
		if newUnit.isHasPromotion(iProm):
			if gc.getPromotionInfo(iProm).isEquipment():
				newUnit.setHasPromotion(iProm, False)
	CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_HERO_RESSURECTED", ()),'AS2D_CHARM_PERSON',1,'Art/Interface/Buttons/Spells/Ressurection.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)

def spellRessurectionGraveyard(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
	iUnit = infoCiv.getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_CHAMPION'))
	if iUnit == -1:
		iUnit = gc.getInfoTypeForString('UNIT_CHAMPION')
	newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	newUnit.changeExperience(CyGame().getSorenRandNum(30, "Ressurection Graveyard"), -1, False, False, False)
	pPlot.setImprovementType(-1)

def reqReveal(caster):
	if caster.isIgnoreHide():
		return False
	pPlot = caster.plot()
	if pPlot.getOwner() != caster.getOwner():
		return False
	return True

def spellReveal(caster):
	caster.setIgnoreHide(True)

def reqRevelry(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isGoldenAge():
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getTotalPopulation() < 25:
			return False
	return True

def spellRevelry(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.changeGoldenAgeTurns(CyGame().goldenAgeLength() * 2)

def reqRevelation(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	iX = caster.getX()
	iY = caster.getY()
	iHidden = gc.getInfoTypeForString('PROMOTION_HIDDEN')
	iHiddenNationality = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
	iIllusion = gc.getInfoTypeForString('PROMOTION_ILLUSION')
	iInvisible = gc.getInfoTypeForString('PROMOTION_INVISIBLE')
	for iiX in range(iX-3, iX+4, 1):
		for iiY in range(iY-3, iY+4, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for iUnit in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit.getTeam() != iTeam:
					if pUnit.isHasPromotion(iHidden):
						return True
					if pUnit.isHasPromotion(iHiddenNationality):
						return True
					if pUnit.isHasPromotion(iInvisible):
						return True
					if pUnit.isHasPromotion(iIllusion):
						return True
	return False

def spellRevelation(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	iX = caster.getX()
	iY = caster.getY()
	iHidden = gc.getInfoTypeForString('PROMOTION_HIDDEN')
	iHiddenNationality = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
	iIllusion = gc.getInfoTypeForString('PROMOTION_ILLUSION')
	iInvisible = gc.getInfoTypeForString('PROMOTION_INVISIBLE')
	for iiX in range(iX-3, iX+4, 1):
		for iiY in range(iY-3, iY+4, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for iUnit in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(iUnit)
				if pUnit.getTeam() != iTeam:
					if pUnit.isHasPromotion(iHidden):
						pUnit.setHasPromotion(iHidden, False)
					if pUnit.isHasPromotion(iHiddenNationality):
						pUnit.setHasPromotion(iHiddenNationality, False)
					if pUnit.isHasPromotion(iInvisible):
						pUnit.setHasPromotion(iInvisible, False)
					if pUnit.isHasPromotion(iIllusion):
						pUnit.kill(True, caster.getOwner())

def spellRingofFlames(caster):
	iX = caster.getX()
	iY = caster.getY()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			if not (iiX == iX and iiY == iY):
				pPlot = CyMap().plot(iiX,iiY)
				bValid = True
				if pPlot.getImprovementType() != -1:
					if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent():
						bValid = False
				if bValid:
					if (pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FOREST') or pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_JUNGLE') or pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FOREST_NEW')):
						if CyGame().getSorenRandNum(100, "Flames Spread") <= gc.getDefineINT('FLAMES_SPREAD_CHANCE'):
							pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_SMOKE'))

def reqRiverOfBlood(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() == 0:
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellRiverOfBlood(caster):
	iOwner = caster.getOwner()
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			if iPlayer != iOwner:
				for pyCity in PyPlayer(iPlayer).getCityList() :
					pCity = pyCity.GetCy()
					if pCity.getPopulation() > 2:
						pCity.changePopulation(-2)
						CyInterface().addMessage(pCity.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_RIVER_OF_BLOOD", ()),'',1,'Art/Interface/Buttons/Spells/River of Blood.dds',ColorTypes(7),pCity.getX(),pCity.getY(),True,True)
			if iPlayer == iOwner:
				for pyCity in PyPlayer(iPlayer).getCityList() :
					pCity = pyCity.GetCy()
					pCity.changePopulation(2)

def reqRoar(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	eTeam = gc.getTeam(pPlayer.getTeam())
	iX = caster.getX()
	iY = caster.getY()
	iTarget = -1
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if not pUnit.isImmuneToFear():
					p2Player = gc.getPlayer(pUnit.getOwner())
					e2Team = p2Player.getTeam()
					if eTeam.isAtWar(e2Team) == True:
						return True
	return False

def spellRoar(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	eTeam = gc.getTeam(pPlayer.getTeam())
	pPlot = caster.plot()
	iX = caster.getX()
	iY = caster.getY()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pLoopPlot = CyMap().plot(iiX,iiY)
			if not pLoopPlot.isNone():
				for i in range(pLoopPlot.getNumUnits() -1, -1, -1):
					pUnit = pLoopPlot.getUnit(i)
					p2Player = gc.getPlayer(pUnit.getOwner())
					i2Team = p2Player.getTeam()
					if eTeam.isAtWar(i2Team):
						if cf.doFear(pUnit, pPlot, caster, True):
							CyInterface().addMessage(pUnit.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FEAR", (gc.getUnitInfo(pUnit.getUnitType()).getDescription(), )),'',1,'Art/Interface/Buttons/Spells/Roar.dds',ColorTypes(7),pUnit.getX(),pUnit.getY(),True,True)
							CyInterface().addMessage(iPlayer,True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FEAR_ENEMY", (gc.getUnitInfo(pUnit.getUnitType()).getDescription(), )),'',1,'Art/Interface/Buttons/Spells/Roar.dds',ColorTypes(8),pUnit.getX(),pUnit.getY(),True,True)

def reqRobGrave(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
			return False
	return True

def spellRobGrave(caster):
	CyGame().changeGlobalCounter(1)
	pPlot = caster.plot()
	pPlot.setImprovementType(-1)
	pPlayer = gc.getPlayer(caster.getOwner())
	lList = ['LOW_GOLD', 'HIGH_GOLD', 'SPAWN_SKELETONS', 'SPAWN_SPECTRE']
	if pPlayer.canReceiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_TECH'), caster):
		lList = lList + ['TECH']
	sGoody = lList[CyGame().getSorenRandNum(len(lList), "Pick Goody")-1]
	if sGoody == 'LOW_GOLD':
		pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_LOW_GOLD'), caster)
	if sGoody == 'HIGH_GOLD':
		pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_HIGH_GOLD'), caster)
	if sGoody == 'TECH':
		pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_TECH'), caster)
	if sGoody == 'SPAWN_SKELETONS':
		pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_SKELETONS'), caster)
	if sGoody == 'SPAWN_SPECTRE':
		pPlayer.receiveGoody(pPlot, gc.getInfoTypeForString('GOODY_GRAVE_SPECTRE'), caster)

def spellSacrificeAltar(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	eTeam = gc.getTeam(pPlayer.getTeam())
	iTech = pPlayer.getCurrentResearch()
	iNum = 10 + (caster.getLevel() * caster.getLevel())
	eTeam.changeResearchProgress(iTech, iNum, caster.getOwner())

def spellSacrificePyre(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	caster.cast(gc.getInfoTypeForString('SPELL_RING_OF_FLAMES'))
	if caster.isImmortal():
		caster.changeImmortal(-1)
	iCount = 1
	if isWorldUnitClass(caster.getUnitClassType()):
		iCount = 7
	for i in range(iCount):
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_FIRE_ELEMENTAL'), caster.getX(), caster.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)

def reqSanctify(caster):
	pPlot = caster.plot()
	bValid = False
	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_CITY_RUINS'):
		return True
	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD'):
		return True
	iX = pPlot.getX()
	iY = pPlot.getY()
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_PLOT_COUNTER):
		iBrokenLands = gc.getInfoTypeForString('TERRAIN_BROKEN_LANDS')
		iBurningSands = gc.getInfoTypeForString('TERRAIN_BURNING_SANDS')
		iFieldsOfPerdition = gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION')
		iShallows = gc.getInfoTypeForString('TERRAIN_SHALLOWS')
		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				pPlot = CyMap().plot(iiX,iiY)
				if not pPlot.isNone():
					iTerrain = pPlot.getTerrainType()
					if (iTerrain == iBrokenLands or iTerrain == iBurningSands or iTerrain == iFieldsOfPerdition or iTerrain == iShallows):
						bValid = True
	else:
		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				pPlot = CyMap().plot(iiX,iiY)
				if not pPlot.isNone():
					if pPlot.getPlotCounter() > 0:
						bValid = True
	if bValid == False:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		if caster.getOwner() != pPlot.getOwner():
			return False
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
			return False
	return True

def spellSanctify(caster):
	pPlot = caster.plot()
	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_CITY_RUINS'):
		pPlot.setImprovementType(-1)
		CyGame().changeGlobalCounter(-1)
	if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_GRAVEYARD'):
		pPlot.setImprovementType(-1)
		CyGame().changeGlobalCounter(-1)
		pPlayer = gc.getPlayer(caster.getOwner())
		newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_EINHERJAR'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	iX = pPlot.getX()
	iY = pPlot.getY()
	if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_PLOT_COUNTER):
		iBrokenLands = gc.getInfoTypeForString('TERRAIN_BROKEN_LANDS')
		iBurningSands = gc.getInfoTypeForString('TERRAIN_BURNING_SANDS')
		iDesert = gc.getInfoTypeForString('TERRAIN_DESERT')
		iFieldsOfPerdition = gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION')
		iGrass = gc.getInfoTypeForString('TERRAIN_GRASS')
		iMarsh = gc.getInfoTypeForString('TERRAIN_MARSH')
		iPlains = gc.getInfoTypeForString('TERRAIN_PLAINS')
		iShallows = gc.getInfoTypeForString('TERRAIN_SHALLOWS')
		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				pPlot = CyMap().plot(iiX,iiY)
				if not pPlot.isNone():
					iTerrain = pPlot.getTerrainType()
					if iTerrain == iBrokenLands:
						pPlot.setTerrainType(iGrass, True, True)
					if iTerrain == iBurningSands:
						pPlot.setTerrainType(iDesert, True, True)
					if iTerrain == iFieldsOfPerdition:
						pPlot.setTerrainType(iPlains, True, True)
					if iTerrain == iShallows:
						pPlot.setTerrainType(iMarsh, True, True)
	else:
		for iiX in range(iX-1, iX+2, 1):
			for iiY in range(iY-1, iY+2, 1):
				pPlot = CyMap().plot(iiX,iiY)
				if pPlot.getPlotCounter() > 0:
					pPlot.changePlotCounter(pPlot.getPlotCounter() * -1)

def reqSanctuary(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getNumCities() == 0:
		return False
	if not pPlayer.isHuman():
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		eTeam = gc.getTeam(iTeam)
		if eTeam.getAtWarCount(True) < 2:
			return False
	return True

def spellSanctuary(caster):
	iPlayer = caster.getOwner()
	iTeam = caster.getTeam()
	pPlayer = gc.getPlayer(iPlayer)
	pPlayer.changeSanctuaryTimer(30)
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		if pPlot.isOwned():
			if pPlot.getOwner() == iPlayer:
				for i in range(pPlot.getNumUnits(), -1, -1):
					pUnit = pPlot.getUnit(i)
					if pUnit.getTeam() != iTeam:
						pUnit.jumpToNearestValidPlot()

def reqSandLion(caster):
	pPlot = caster.plot()
	if (pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_DESERT') and pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_BURNING_SANDS')):
		return False
	return True

def reqScorch(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	if (pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS') or pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION')):
		if pPlayer.isHuman() == False:
			if caster.getOwner() == pPlot.getOwner():
				return False
		return True
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
		if pPlayer.isHuman() == False:
			if caster.getOwner() != pPlot.getOwner():
				return False
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				return False
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
				return False
		return True	
	return False

def spellScorch(caster):
	pPlot = caster.plot()
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS'):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_DESERT'),True,True)
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION'):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_BURNING_SANDS'),True,True)
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SNOW'):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_TUNDRA'),True,True)
	if pPlot.isOwned():
		cf.startWar(caster.getOwner(), pPlot.getOwner(), WarPlanTypes.WARPLAN_TOTAL)

def spellSing(caster):
	pPlot = caster.plot()
	point = pPlot.getPoint()
	iRnd = CyGame().getSorenRandNum(100, "Sing")
	szText = "AS3D_SING1"
	if iRnd > 25:
		szText = "AS3D_SING2"
	if iRnd > 50:
		szText = "AS3D_SING3"
	if iRnd > 75:
		szText = "AS3D_SING4"
	CyAudioGame().Play3DSound(szText,point.x,point.y,point.z)

def reqSironasTouch(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_HEAL_UNIT_PER_TURN) == false:
		return False
	if caster.getDamage() == 0:
		return False
	if pPlayer.isHuman() == False:
		if caster.getDamage() < 15:
			return False
	return True

def spellSironasTouch(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlayer.setFeatAccomplished(FeatTypes.FEAT_HEAL_UNIT_PER_TURN, false)
	caster.changeDamage(-15,0)

def spellSlaveTradeBuy(caster):
	pCity = caster.plot().getPlotCity()
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	newUnit = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_SLAVE'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
	iPromotion = -1
	iRnd = CyGame().getSorenRandNum(100, "Slave Trade Buy")
	if (iRnd >= 60 and iRnd < 70):
		iPromotion = gc.getInfoTypeForString('PROMOTION_DWARF')
	if (iRnd >= 70 and iRnd < 80):
		iPromotion = gc.getInfoTypeForString('PROMOTION_ELF')
	if (iRnd >= 80):
		iPromotion = gc.getInfoTypeForString('PROMOTION_ORC')
	if iPromotion != -1:
		newUnit.setHasPromotion(iPromotion, True)

def spellSnowfall(caster):
	iX = caster.getX()
	iY = caster.getY()
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot = CyMap().plot(iiX,iiY)
			if not pPlot.isNone():
				if not pPlot.isWater():
					if pPlot.getTerrainType() != iSnow:
						iRnd = CyGame().getSorenRandNum(6, "Snowfall") + 3
						pPlot.setTempTerrainType(iSnow, iRnd)
						if pPlot.getFeatureType() == iFlames:
							pPlot.setFeatureType(-1, -1)
						if pPlot.getImprovementType() == iSmoke:
							pPlot.setImprovementType(-1)

def spellSnowfallGreator(caster):
	iX = caster.getX()
	iY = caster.getY()
	iFlames = gc.getInfoTypeForString('FEATURE_FLAMES')
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	iSnow = gc.getInfoTypeForString('TERRAIN_SNOW')
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot = CyMap().plot(iiX,iiY)
			if not pPlot.isNone():
				if not pPlot.isWater():
					if pPlot.getTerrainType() != iSnow:
						iRnd = CyGame().getSorenRandNum(12, "Snowfall") + 6
						pPlot.setTempTerrainType(iSnow, iRnd)
						if pPlot.getFeatureType() == iFlames:
							pPlot.setFeatureType(-1, -1)
						if pPlot.getImprovementType() == iSmoke:
							pPlot.setImprovementType(-1)

def reqSpreadTheCouncilOfEsus(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = caster.plot().getPlotCity()
	if pCity.isHasReligion(gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS')):
		return False
	if pPlayer.isHuman() == False:
		if pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'):
			return False
	return True

def reqSpring(caster):
	pPlot = caster.plot()
	pPlayer = gc.getPlayer(caster.getOwner())
	bFlames = false
	iX = pPlot.getX()
	iY = pPlot.getY()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if pPlot2.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLAMES') or pPlot2.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SMOKE'):
				bFlames = true
	if bFlames == False:
		if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_DESERT'):
			return False
		if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS'):
			return False
		if pPlayer.isHuman() == False:
			if caster.getOwner() != pPlot.getOwner():
				return False
	if pPlayer.isHuman() == False:
		if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
			return False
	return True

def spellSpring(caster):
	pPlot = caster.plot()
	if (pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT') and pPlot.getFeatureType() != gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
		if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_SCRUB'):
			pPlot.setFeatureType(-1, -1)
	iX = pPlot.getX()
	iY = pPlot.getY()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pPlot2 = CyMap().plot(iiX,iiY)
			if pPlot2.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLAMES'):
				pPlot2.setFeatureType(-1, -1)
			if pPlot2.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SMOKE'):
				pPlot2.setImprovementType(-1)

def reqSprint(caster):
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FATIGUED')):
		return False
	return True

def reqStasis(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getNumCities() < 5:
			return False
	return True

def spellStasis(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	iDelay = 20
	iTeam = pPlayer.getTeam()
	if CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_QUICK'):
		iDelay = 14
	if CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_EPIC'):
		iDelay = 30
	if CyGame().getGameSpeedType() == gc.getInfoTypeForString('GAMESPEED_MARATHON'):
		iDelay = 60
	for iPlayer2 in range(gc.getMAX_PLAYERS()):
		pPlayer2 = gc.getPlayer(iPlayer2)
		if pPlayer2.isAlive():
			if pPlayer2.getTeam() != iTeam:
				pPlayer2.changeDisableProduction(iDelay)
				pPlayer2.changeDisableResearch(iDelay)

def reqSteal(caster):
	iTeam = caster.getTeam()
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getTeam() != iTeam:
			for iProm in range(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(iProm):
					if gc.getPromotionInfo(iProm).isEquipment():
						return True
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getTeam() != iTeam:
			for iBuild in range(gc.getNumBuildingInfos()):
				if pCity.getNumRealBuilding(iBuild) > 0:
					if gc.getBuildingInfo(iBuild).isEquipment():
						return True
	return False

def spellSteal(caster):
	iTeam = caster.getTeam()
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getTeam() != iTeam:
			for iProm in range(gc.getNumPromotionInfos()):
				if pUnit.isHasPromotion(iProm):
					if gc.getPromotionInfo(iProm).isEquipment():
 						if CyGame().getSorenRandNum(100, "Steal") <= 20:
							cf.startWar(caster.getOwner(), pUnit.getOwner(), WarPlanTypes.WARPLAN_TOTAL)
						else:
							caster.setHasPromotion(iProm, True)
							pUnit.setHasPromotion(iProm, False)
	if pPlot.isCity():
		pCity = pPlot.getPlotCity()
		if pCity.getTeam() != iTeam:
			for iBuild in range(gc.getNumBuildingInfos()):
				if pCity.getNumRealBuilding(iBuild) > 0:
					if gc.getBuildingInfo(iBuild).isEquipment():
 						if CyGame().getSorenRandNum(100, "Steal") <= 20:
							cf.startWar(caster.getOwner(), pUnit.getOwner(), WarPlanTypes.WARPLAN_TOTAL)
						else:
							for iUnit in range(gc.getNumUnitInfos()):
								if gc.getUnitInfo(iUnit).getBuildings(iBuild):
									pCity.setNumRealBuilding(iBuild, 0)
									caster.setHasPromotion(gc.getUnitInfo(iUnit).getEquipmentPromotion(), True)

def reqTakeEquipmentBuilding(caster,unit):
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
		return False
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
		return False
	if caster.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_SPELL'):
		return False
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION')):
		return False
	iUnit = gc.getInfoTypeForString(unit)
	iProm = gc.getUnitInfo(iUnit).getEquipmentPromotion()
	if caster.isHasPromotion(iProm):
		return False
	return True

def spellTakeEquipmentBuilding(caster,unit):
	iUnit = gc.getInfoTypeForString(unit)
	pPlot = caster.plot()
	for i in range(gc.getNumBuildingInfos()):
		if gc.getUnitInfo(iUnit).getBuildings(i):
			pPlot.getPlotCity().setNumRealBuilding(i, 0)

def reqTakeEquipmentPromotion(caster,unit):
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
		return False
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
		return False
	if caster.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_SPELL'):
		return False
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION')):
		return False
	iUnit = gc.getInfoTypeForString(unit)
	iProm = gc.getUnitInfo(iUnit).getEquipmentPromotion()
	if caster.isHasPromotion(iProm):
		return False
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	pHolder = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getOwner() == iPlayer and pUnit.isHasPromotion(iProm)):
			pHolder = pUnit
	if pHolder == -1:
		return False
	if pHolder.isHasCasted():
		return False
	if pHolder.getUnitType() == gc.getInfoTypeForString('UNIT_BARNAXUS'):
		if iProm == gc.getInfoTypeForString('PROMOTION_PIECES_OF_BARNAXUS'):
			return False
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.isHuman() == False:
		if caster.baseCombatStr() - 2 <= pHolder.baseCombatStr():
			return False
		if gc.getUnitInfo(pHolder.getUnitType()).getFreePromotions(iProm):
			return False
	return True

def spellTakeEquipmentPromotion(caster,unit):
	iUnit = gc.getInfoTypeForString(unit)
	iProm = gc.getUnitInfo(iUnit).getEquipmentPromotion()
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	pHolder = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getOwner() == iPlayer and pUnit.isHasPromotion(iProm) and pUnit != caster):
			pHolder = pUnit
	if pHolder != -1:
		pHolder.setHasPromotion(iProm, False)
		caster.setHasPromotion(iProm, True)

def reqTakeEquipmentUnit(caster,unit):
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_NAVAL'):
		return False
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_SIEGE'):
		return False
	if caster.getSpecialUnitType() == gc.getInfoTypeForString('SPECIALUNIT_SPELL'):
		return False
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ILLUSION')):
		return False
	iUnit = gc.getInfoTypeForString(unit)
	iProm = gc.getUnitInfo(iUnit).getEquipmentPromotion()
	if caster.isHasPromotion(iProm):
		return False
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	pHolder = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getOwner() == iPlayer and pUnit.getUnitType() == iUnit):
			if pUnit.isDelayedDeath() == False:
				pHolder = pUnit
	if pHolder == -1:
		return False
	return True

def spellTakeEquipmentUnit(caster,unit):
	iUnit = gc.getInfoTypeForString(unit)
	iProm = gc.getUnitInfo(iUnit).getEquipmentPromotion()
	iPlayer = caster.getOwner()
	pPlot = caster.plot()
	pHolder = -1
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if (pUnit.getOwner() == iPlayer and pUnit.getUnitType() == iUnit):
			if pUnit.isDelayedDeath() == False:
				pHolder = pUnit
	if pHolder != -1:
		pHolder.kill(True, PlayerTypes.NO_PLAYER)

def reqTaunt(caster):
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	bValid = False
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pLoopPlot = CyMap().plot(iiX,iiY)
			for i in range(pLoopPlot.getNumUnits()):
				pUnit = pLoopPlot.getUnit(i)
				if eTeam.isAtWar(pUnit.getTeam()):
					if pUnit.isAlive():
						if pUnit.canAttack():
							if caster.getDomainType() == pUnit.getDomainType():
								bValid = True
	return bValid

def spellTaunt(caster):
	iEnraged = gc.getInfoTypeForString('PROMOTION_ENRAGED')
	iSpell = gc.getInfoTypeForString('SPELL_TAUNT')
	iX = caster.getX()
	iY = caster.getY()
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	iTeam = pPlayer.getTeam()
	eTeam = gc.getTeam(iTeam)
	bValid = False
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			pLoopPlot = CyMap().plot(iiX,iiY)
			for i in range(pLoopPlot.getNumUnits()):
				pUnit = pLoopPlot.getUnit(i)
				if eTeam.isAtWar(pUnit.getTeam()):
					if pUnit.isAlive():
						if pUnit.canAttack():
							if caster.getDomainType() == pUnit.getDomainType():
								if not pUnit.isResisted(caster, iSpell):
									pUnit.attack(pPlot, False)

def spellTeleport(caster,loc):
	player = caster.getOwner()
	pPlayer = gc.getPlayer(player)
	pCity = pPlayer.getCapitalCity()
	caster.setXY(pCity.getX(), pCity.getY(), false, true, true)

def reqTeachSpellcasting(caster):
	iAnimal = gc.getInfoTypeForString('UNITCOMBAT_ANIMAL')
	iBird = gc.getInfoTypeForString('SPECIALUNIT_BIRD')
	lList = []
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_AIR1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BODY1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_BODY1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_CHAOS1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_DEATH1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_EARTH1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_ENTROPY1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_FIRE1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ICE1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_ICE1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LAW1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_LAW1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_LIFE1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_METAMAGIC1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_MIND1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_NATURE1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_SHADOW1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_SPIRIT1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_SUN1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_WATER1')]
	if len(lList) > 0:
		pPlot = caster.plot()
		iPlayer = caster.getOwner()
		for i in range(pPlot.getNumUnits()):
			pUnit = pPlot.getUnit(i)
			if pUnit.getOwner() == iPlayer:
				if pUnit.isAlive():
					if pUnit.getUnitCombatType() != iAnimal:
						if pUnit.getSpecialUnitType() != iBird:
							for iProm in range(len(lList)):
								if not pUnit.isHasPromotion(lList[iProm]):
									return True
	return False

def spellTeachSpellcasting(caster):
	iAnimal = gc.getInfoTypeForString('UNITCOMBAT_ANIMAL')
	iBird = gc.getInfoTypeForString('SPECIALUNIT_BIRD')
	iChanneling1 = gc.getInfoTypeForString('PROMOTION_CHANNELING1')
	lList = []
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_AIR1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_BODY1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_BODY1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_CHAOS1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_DEATH1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_EARTH1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_EARTH1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_ENCHANTMENT1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_ENTROPY1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_FIRE1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ICE1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_ICE1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LAW1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_LAW1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_LIFE1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_METAMAGIC1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_MIND1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_NATURE1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_NATURE1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_SHADOW1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SPIRIT1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_SPIRIT1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_SUN1')]
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1')):
		lList = lList + [gc.getInfoTypeForString('PROMOTION_WATER1')]
	pPlot = caster.plot()
	iPlayer = caster.getOwner()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getOwner() == iPlayer:
			if pUnit.isAlive():
				if pUnit.getUnitCombatType() != iAnimal:
					if pUnit.getSpecialUnitType() != iBird:
						for iProm in range(len(lList)):
							if not pUnit.isHasPromotion(lList[iProm]):
								pUnit.setHasPromotion(lList[iProm], True)
								if not pUnit.isHasPromotion(iChanneling1):
									pUnit.setHasPromotion(iChanneling1, True)

def spellTreetopDefence(caster):
	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if pUnit.getTeam() == caster.getTeam():
			pUnit.setFortifyTurns(5)

def reqTrust(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isFeatAccomplished(FeatTypes.FEAT_TRUST):
		return False
	if pPlayer.isBarbarian():
		return False
	return True

def spellTrust(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	pCity = pPlayer.getCapitalCity()
	pPlayer.setFeatAccomplished(FeatTypes.FEAT_TRUST, true)

def spellTsunami(caster):
	iX = caster.getX()
	iY = caster.getY()
	for iiX in range(iX-2, iX+3, 1):
		for iiY in range(iY-2, iY+3, 1):
			pPlot = CyMap().plot(iiX,iiY)
			if pPlot.isAdjacentToWater():
				if (iX != iiX or iY != iiY):
					for i in range(pPlot.getNumUnits()):
						pUnit = pPlot.getUnit(i)
						pUnit.doDamage(0, 75, caster, gc.getInfoTypeForString('DAMAGE_COLD'), true)
					if pPlot.getImprovementType() != -1:
						if gc.getImprovementInfo(pPlot.getImprovementType()).isPermanent() == False:
							if CyGame().getSorenRandNum(100, "Tsunami") <= 25:
								pPlot.setImprovementType(-1)
					CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPRING'),pPlot.getPoint())

def spellUnyieldingOrder(caster):
	pPlot = caster.plot()
	pCity = pPlot.getPlotCity()
	pCity.setOccupationTimer(0)
	pCity.changeHurryAngerTimer(-9)

def reqUpgradeDovielloWarrior(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if not pPlayer.isHuman():
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		eTeam = gc.getTeam(iTeam)
		if eTeam.getAtWarCount(True) == 0:
			return False
		if pPlayer.getNumCities() > pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_WORKER')):
			return False
	return True

def reqVeilOfNight(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getNumUnits() < 25:
			return False
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		eTeam = gc.getTeam(iTeam)
		if eTeam.getAtWarCount(True) > 0:
			return False
	return True

def spellVeilOfNight(caster):
	iHiddenNationality = gc.getInfoTypeForString('PROMOTION_HIDDEN_NATIONALITY')
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.baseCombatStr() > 0:
			pUnit.setHasPromotion(iHiddenNationality, True)

def reqVitalize(caster):
	pPlot = caster.plot()
	if pPlot.getOwner() != caster.getOwner():
		return False
	if pPlot.isWater():
		return false
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_GRASS'):
		return False
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BURNING_SANDS'):
		return False
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BROKEN_LANDS'):
		return False
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION'):
		return False
	if pPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_MARSH'):
		return False
	return True

def spellVitalize(caster):
	pPlot = caster.plot()
	if(pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_SNOW')):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_TUNDRA'),True,True)
	elif(pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_TUNDRA')):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
	elif(pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_DESERT')):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_PLAINS'),True,True)
		if pPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_SCRUB'):
			pPlot.setFeatureType(-1, -1)
	elif(pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_PLAINS')):
		pPlot.setTerrainType(gc.getInfoTypeForString('TERRAIN_GRASS'),True,True)

def reqWane(caster):
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ANIMAL'):
		return False
	if caster.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_BEAST'):
		return False
	if caster.isImmortal():
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_SHADE')) >= 4:
		return False
	return True

def reqWarcry(caster):
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if pPlayer.getNumUnits() < 25:
			return False
		iTeam = gc.getPlayer(caster.getOwner()).getTeam()
		eTeam = gc.getTeam(iTeam)
		if eTeam.getAtWarCount(True) == 0:
			return False
	return True

def spellWarcry(caster):
	iWarcry = gc.getInfoTypeForString('PROMOTION_WARCRY')
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.getUnitCombatType() != -1:
			pUnit.setHasPromotion(iWarcry, True)

def reqWhiteout(caster):
	pPlot = caster.plot()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_HIDDEN')):
		return False
	if pPlot.getTerrainType() != gc.getInfoTypeForString('TERRAIN_SNOW'):
		return False
	return True

def reqWildHunt(caster):
	iPlayer = caster.getOwner()
	pPlayer = gc.getPlayer(iPlayer)
	if pPlayer.isHuman() == False:
		iTeam = gc.getPlayer(iPlayer).getTeam()
		eTeam = gc.getTeam(iTeam)
		if eTeam.getAtWarCount(True) == 0:
			return False
		if pPlayer.getNumUnits() < 20:
			return False
	return True

def spellWildHunt(caster):
	iWolf = gc.getInfoTypeForString('UNIT_WOLF')
	pPlayer = gc.getPlayer(caster.getOwner())
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.baseCombatStr() > 0:
			newUnit = pPlayer.initUnit(iWolf, pUnit.getX(), pUnit.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pUnit.baseCombatStr() > 3:
				i = (pUnit.baseCombatStr() - 2) / 2
				newUnit.setBaseCombatStr(2 + i)

def spellWonder(caster):
	iCount = CyGame().getSorenRandNum(3, "Wonder") + 3
	pPlayer = gc.getPlayer(caster.getOwner())
	pPlot = caster.plot()
	bCity = False
	point = pPlot.getPoint()
	if pPlot.isCity():
		bCity = True
	for i in range (iCount):
		iRnd = CyGame().getSorenRandNum(66, "Wonder")
		iUnit = -1
		if iRnd == 0:
			caster.cast(gc.getInfoTypeForString('SPELL_BLAZE'))
		if iRnd == 1:
			caster.cast(gc.getInfoTypeForString('SPELL_BLESS'))
		if iRnd == 2:
			caster.cast(gc.getInfoTypeForString('SPELL_BLINDING_LIGHT'))
		if iRnd == 3:
			caster.cast(gc.getInfoTypeForString('SPELL_BLOOM'))
		if iRnd == 4:
			caster.cast(gc.getInfoTypeForString('SPELL_BLUR'))
		if iRnd == 5:
			caster.cast(gc.getInfoTypeForString('SPELL_CHARM_PERSON'))
		if iRnd == 6:
			caster.cast(gc.getInfoTypeForString('SPELL_CONTAGION'))
		if iRnd == 7:
			caster.cast(gc.getInfoTypeForString('SPELL_COURAGE'))
		if iRnd == 8:
			caster.cast(gc.getInfoTypeForString('SPELL_CRUSH'))
		if iRnd == 9:
			caster.cast(gc.getInfoTypeForString('SPELL_DESTROY_UNDEAD'))
		if iRnd == 10:
			caster.cast(gc.getInfoTypeForString('SPELL_DISPEL_MAGIC'))
		if iRnd == 11:
			caster.cast(gc.getInfoTypeForString('SPELL_EARTHQUAKE'))
		if iRnd == 12:
			caster.cast(gc.getInfoTypeForString('SPELL_ENCHANTED_BLADE'))
		if iRnd == 13:
			CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL1'),point)
			CyAudioGame().Play3DSound("AS3D_SPELL_DEFILE",point.x,point.y,point.z)
			for iX in range(pPlot.getX()-1, pPlot.getX()+2, 1):
				for iY in range(pPlot.getY()-1, pPlot.getY()+2, 1):
					pLoopPlot = CyMap().plot(iX,iY)
					if pLoopPlot.isNone() == False:
						pLoopPlot.changePlotCounter(100)
		if iRnd == 14:
			caster.cast(gc.getInfoTypeForString('SPELL_ENTANGLE'))
		if iRnd == 15:
			if caster.getOwner() != gc.getBARBARIAN_PLAYER():
				caster.cast(gc.getInfoTypeForString('SPELL_ESCAPE'))
		if iRnd == 16:
			caster.cast(gc.getInfoTypeForString('SPELL_FIREBALL'))
		if iRnd == 17:
			caster.cast(gc.getInfoTypeForString('SPELL_FLAMING_ARROWS'))
		if iRnd == 18:
			caster.cast(gc.getInfoTypeForString('SPELL_FLOATING_EYE'))
		if iRnd == 19:
			caster.cast(gc.getInfoTypeForString('SPELL_HASTE'))
		if iRnd == 20:
			caster.cast(gc.getInfoTypeForString('SPELL_HASTURS_RAZOR'))
		if iRnd == 21:
			caster.cast(gc.getInfoTypeForString('SPELL_HEAL'))
		if iRnd == 22:
			caster.cast(gc.getInfoTypeForString('SPELL_HIDE'))
		if iRnd == 23:
			caster.cast(gc.getInfoTypeForString('SPELL_LOYALTY'))
		if iRnd == 24:
			caster.cast(gc.getInfoTypeForString('SPELL_MAELSTROM'))
		if iRnd == 25:
			caster.cast(gc.getInfoTypeForString('SPELL_MORALE'))
		if iRnd == 26:
			caster.cast(gc.getInfoTypeForString('SPELL_MUTATION'))
		if iRnd == 27:
			caster.cast(gc.getInfoTypeForString('SPELL_PILLAR_OF_FIRE'))
		if iRnd == 28:
			caster.cast(gc.getInfoTypeForString('SPELL_POISONED_BLADE'))
		if iRnd == 29:
			caster.cast(gc.getInfoTypeForString('SPELL_REVELATION'))
		if iRnd == 30:
			caster.cast(gc.getInfoTypeForString('SPELL_RING_OF_FLAMES'))
		if iRnd == 31:
			caster.cast(gc.getInfoTypeForString('SPELL_RUST'))
		if iRnd == 32:
			caster.cast(gc.getInfoTypeForString('SPELL_SANCTIFY'))
		if iRnd == 33:
			caster.cast(gc.getInfoTypeForString('SPELL_SCORCH'))
		if iRnd == 34:
			caster.cast(gc.getInfoTypeForString('SPELL_SHADOWWALK'))
		if iRnd == 35:
			caster.cast(gc.getInfoTypeForString('SPELL_SPORES'))
		if iRnd == 36:
			caster.cast(gc.getInfoTypeForString('SPELL_SPRING'))
		if iRnd == 37:
			caster.cast(gc.getInfoTypeForString('SPELL_STONESKIN'))
		if iRnd == 38:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_AIR_ELEMENTAL'))
		if iRnd == 39:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_AUREALIS'))
		if iRnd == 40:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_BALOR'))
		if iRnd == 41:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_DJINN'))
		if iRnd == 42:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_EARTH_ELEMENTAL'))
		if iRnd == 43:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_EINHERJAR'))
		if iRnd == 44:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_FIRE_ELEMENTAL'))
		if iRnd == 45:
			iUnit = gc.getInfoTypeForString('UNIT_KRAKEN')
		if iRnd == 46:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_MISTFORM'))
		if iRnd == 47:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_PIT_BEAST'))
		if iRnd == 48:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_SAND_LION'))
		if iRnd == 49:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_SPECTRE'))
		if iRnd == 50:
			iUnit = gc.getInfoTypeForString('UNIT_TIGER')
		if iRnd == 51:
			iUnit = gc.getInfoTypeForString('UNIT_TREANT')
		if iRnd == 52:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_WATER_ELEMENTAL'))
		if iRnd == 53:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_WRAITH'))
		if iRnd == 54:
			caster.cast(gc.getInfoTypeForString('SPELL_TSUNAMI'))
		if iRnd == 55:
			caster.cast(gc.getInfoTypeForString('SPELL_VALOR'))
		if iRnd == 56:
			caster.cast(gc.getInfoTypeForString('SPELL_VITALIZE'))
		if iRnd == 57:
			caster.cast(gc.getInfoTypeForString('SPELL_WITHER'))
		if iRnd == 58:
			if bCity == False:
				iImprovement = pPlot.getImprovementType()
				bValid = True
				if iImprovement != -1 :
					if gc.getImprovementInfo(iImprovement).isPermanent() :
						bValid = False
				if bValid :
					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_PENGUINS'))
					CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_PENGUINS", ()),'',1,'Art/Interface/Buttons/Improvements/Penguins.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		if iRnd == 59:
			if bCity == False:
				iImprovement = pPlot.getImprovementType()
				bValid = True
				if iImprovement != -1 :
					if gc.getImprovementInfo(iImprovement).isPermanent() :
						bValid = False
				if bValid :
					pPlot.setImprovementType(gc.getInfoTypeForString('IMPROVEMENT_MUSHROOMS'))
					CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_MUSHROOMS", ()),'',1,'Art/Interface/Buttons/Improvements/Mushrooms.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		if iRnd == 60:
			for iProm in range(gc.getNumPromotionInfos()):
				if caster.isHasPromotion(iProm):
					if gc.getPromotionInfo(iProm).isRace():
						caster.setHasPromotion(iProm, False)
			caster.setUnitArtStyleType(gc.getInfoTypeForString('UNIT_ARTSTYLE_BABOON'))
			CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_BABOON", ()),'',1,'Art/Interface/Buttons/Units/Margalard.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
			if pPlayer.isHuman():
				t = "TROPHY_FEAT_BABOON"
				if not CyGame().isHasTrophy(t):
					CyGame().changeTrophyValue(t, 1)
		if iRnd == 61:
			CyEngine().triggerEffect(gc.getInfoTypeForString('EFFECT_SPELL1'),point)
			CyAudioGame().Play3DSound("AS3D_SPELL_SANCTIFY",point.x,point.y,point.z)
			for iX in range(pPlot.getX()-2, pPlot.getX()+3, 1):
				for iY in range(pPlot.getY()-2, pPlot.getY()+3, 1):
					pLoopPlot = CyMap().plot(iX,iY)
					if pLoopPlot.isNone() == False:
						pLoopPlot.changePlotCounter(-100)
		if iRnd == 62:
			iUnit = gc.getInfoTypeForString('UNIT_SPIDERKIN')
			CyInterface().addMessage(caster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WONDER_SPIDERKIN", ()),'',1,'Art/Interface/Buttons/Units/Spiderkin.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		if iUnit != -1:
			newUnit = pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SUMMONER')):
				newUnit.setDuration(2)
			else:
				newUnit.setDuration(1)
		if iRnd == 63:
			caster.cast(gc.getInfoTypeForString('SPELL_SLOW'))
		if iRnd == 64:
			caster.cast(gc.getInfoTypeForString('SPELL_SUMMON_ICE_ELEMENTAL'))
		if iRnd == 65:
			caster.cast(gc.getInfoTypeForString('SPELL_SNOWFALL'))

def reqWorldbreak(caster):
	if CyGame().getGlobalCounter() == 0:
		return False
	pPlayer = gc.getPlayer(caster.getOwner())
	if pPlayer.isHuman() == False:
		if CyGame().getGlobalCounter() < 50:
			return False
	return True

def spellWorldbreak(caster):
	iCounter = CyGame().getGlobalCounter()
	iFire = gc.getInfoTypeForString('DAMAGE_FIRE')
	iForest = gc.getInfoTypeForString('FEATURE_FOREST')
	iJungle = gc.getInfoTypeForString('FEATURE_JUNGLE')
	iPillar = gc.getInfoTypeForString('EFFECT_PILLAR_OF_FIRE')
	iSmoke = gc.getInfoTypeForString('IMPROVEMENT_SMOKE')
	for i in range (CyMap().numPlots()):
		pPlot = CyMap().plotByIndex(i)
		bValid = True
		if pPlot.isOwned():
			if pPlot.getOwner() == caster.getOwner():
				bValid = False
		if bValid:
			if pPlot.isCity():
				if CyGame().getSorenRandNum(100, "Worldbreak") <= (iCounter / 4):
					cf.doCityFire(pPlot.getPlotCity())
				for i in range(pPlot.getNumUnits()):
					pUnit = pPlot.getUnit(i)
					pUnit.doDamage(iCounter, 100, caster, iFire, false)
				CyEngine().triggerEffect(iPillar,pPlot.getPoint())
			if (pPlot.getFeatureType() == iForest or pPlot.getFeatureType() == iJungle):
				if pPlot.getImprovementType() == -1:
					if CyGame().getSorenRandNum(100, "Flames Spread") <= (iCounter / 4):
						pPlot.setImprovementType(iSmoke)

def atRangeGuardian(pCaster, pPlot):
	if pPlot.getNumUnits() == 0:
		if CyGame().getStartTurn() + 20 < CyGame().getGameTurn(): #fixes a problem if units spawn next to the gargoyle
			iPlayer = pCaster.getOwner()
			if iPlayer != gc.getBARBARIAN_PLAYER():
				bPlayer = gc.getPlayer(gc.getBARBARIAN_PLAYER())
				iUnit = gc.getInfoTypeForString('UNIT_GARGOYLE')
				newUnit1 = bPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit1.setUnitAIType(gc.getInfoTypeForString('UNITAI_ANIMAL'))
				newUnit2 = bPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit2.setUnitAIType(gc.getInfoTypeForString('UNITAI_ANIMAL'))
				newUnit3 = bPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
				newUnit3.setUnitAIType(gc.getInfoTypeForString('UNITAI_ANIMAL'))
				CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_GUARDIAN", ()),'',1,gc.getUnitInfo(iUnit).getButton(),ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
				pPlot.setPythonActive(False)

def atRangeJungleAltar(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.atRangeJungleAltar(pCaster, pPlot)

def atRangeNecrototem(pCaster, pPlot):
	if cf.doFear(pCaster, pPlot, -1, False):
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_FEAR", (gc.getUnitInfo(pCaster.getUnitType()).getDescription(), )),'',1,'Art/Interface/Buttons/Improvements/Necrototem.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def onMoveAncientForest(pCaster, pPlot):
	if pPlot.isOwned():
		if pPlot.getNumUnits() == 1:
			if pCaster.isFlying() == False:
				iChance = gc.getDefineINT('TREANT_SPAWN_CHANCE')
				if pPlot.isBeingWorked():
					pCity = pPlot.getWorkingCity()
					if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES')) > 0:
						iChance = iChance * 3
				if CyGame().getSorenRandNum(100, "Treant Spawn Chance") <= iChance:
					pPlayer = gc.getPlayer(pCaster.getOwner())
					p2Player = gc.getPlayer(pPlot.getOwner())
					eTeam = gc.getTeam(pPlayer.getTeam())
					i2Team = p2Player.getTeam()
					if (eTeam.isAtWar(i2Team) and p2Player.getStateReligion() == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')):
						for i in range(pPlot.getNumUnits()):
							p2Unit = pPlot.getUnit(i)
							p2Plot = cf.findClearPlot(p2Unit, -1)
							if p2Plot != -1:
								p2Unit.setXY(p2Plot.getX(),p2Plot.getY(), false, true, true)
								p2Unit.finishMoves()
						if pPlot.getNumUnits() == 0:
							newUnit = p2Player.initUnit(gc.getInfoTypeForString('UNIT_TREANT'), pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
							newUnit.setDuration(3)
							CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TREANT_ENEMY",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Units/Treant.dds',ColorTypes(7),newUnit.getX(),newUnit.getY(),True,True)
							CyInterface().addMessage(pPlot.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_TREANT",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Units/Treant.dds',ColorTypes(8),newUnit.getX(),newUnit.getY(),True,True)

def onMoveBlizzard(pCaster, pPlot):
	if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WINTERBORN')) == False:
		pCaster.doDamage(10, 50, pCaster, gc.getInfoTypeForString('DAMAGE_COLD'), false)

def onMoveLetumFrigus(pCaster, pPlot):
	pPlayer = gc.getPlayer(pCaster.getOwner())
	if pPlayer.isHuman():
		iEvent = CvUtil.findInfoTypeNum(gc.getEventTriggerInfo, gc.getNumEventTriggerInfos(),'EVENTTRIGGER_LETUM_FRIGUS')
		triggerData = pPlayer.initTriggeredData(iEvent, true, -1, pCaster.getX(), pCaster.getY(), pCaster.getOwner(), -1, -1, -1, -1, -1)
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_LETUM_FRIGUS", ()),'',1,'Art/Interface/Buttons/Improvements/Letum Frigus.dds',ColorTypes(8),pPlot.getX(),pPlot.getY(),True,True)
		pPlot.setPythonActive(False)

def onMoveMaelstrom(pCaster, pPlot):
	if CyGame().getSorenRandNum(100, "Maelstrom") <= 25:
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_KILL",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pPlot.getX(),pPlot.getY(),True,True)
		pCaster.kill(True, PlayerTypes.NO_PLAYER)
	else:
		iOcean = gc.getInfoTypeForString('TERRAIN_OCEAN')
		iBestValue = 0
		pBestPlot = -1
		for i in range (CyMap().numPlots()):
			iValue = 0
			pTargetPlot = CyMap().plotByIndex(i)
			if pTargetPlot.getTerrainType() == iOcean:
				iValue = CyGame().getSorenRandNum(1000, "Maelstrom")
				if pTargetPlot.isOwned() == false:
					iValue += 1000
				if iValue > iBestValue:
					iBestValue = iValue
					pBestPlot = pTargetPlot
		if pBestPlot != -1:
			pCaster.setXY(pBestPlot.getX(), pBestPlot.getY(), false, true, true)
			pCaster.setDamage(25, PlayerTypes.NO_PLAYER)
			CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_MAELSTROM_MOVE",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Maelstrom.dds',ColorTypes(7),pCaster.getX(),pCaster.getY(),True,True)

def onMoveMirrorOfHeaven(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMoveMirrorOfHeaven(pCaster, pPlot)

def onMovePoolOfTears(pCaster, pPlot):
	if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DISEASED')):
		pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_DISEASED'), false)
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_DISEASED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Pool of Tears.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
	if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED')):
		pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_PLAGUED'), false)
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_PLAGUED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Pool of Tears.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
	if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED')):
		pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_POISONED'), false)
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_POISONED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Pool of Tears.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)
	if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WITHERED')):
		pCaster.setHasPromotion(gc.getInfoTypeForString('PROMOTION_WITHERED'), false)
		CyInterface().addMessage(pCaster.getOwner(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_POOL_OF_TEARS_WITHERED",()),'AS2D_FEATUREGROWTH',1,'Art/Interface/Buttons/Improvements/Pool of Tears.dds',ColorTypes(8),pCaster.getX(),pCaster.getY(),True,True)

def onMoveJungleAltar(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMoveJungleAltar(pCaster, pPlot)

def onMovePortal(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMovePortal(pCaster, pPlot)

def onMoveWarningPost(pCaster, pPlot):
	if CyGame().getWBMapScript():
		sf.onMoveWarningPost(pCaster, pPlot)

def voteFundDissidents():
	iOvercouncil = gc.getInfoTypeForString('DIPLOVOTE_OVERCOUNCIL')
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			if pPlayer.isFullMember(iOvercouncil):
				for pyCity in PyPlayer(iPlayer).getCityList() :
					if CyGame().getSorenRandNum(100, "Fund Dissidents") < 50:
						pCity = pyCity.GetCy()
						pCity.changeHurryAngerTimer(1 + CyGame().getSorenRandNum(3, "Fund Dissidents"))
						
### FW Changes

def reqBuilding(caster,sBuilding,sPromotion):
	pCity = caster.plot().getPlotCity()

	if pCity.getNumRealBuilding(gc.getInfoTypeForString(sBuilding)) == 0:
		return False

	if caster.isHasPromotion(gc.getInfoTypeForString(sPromotion)):
		return False

	if pCity.isSettlement() == True:
		return False

	# TODO: Evaluate Removing This
	#strCheckData = pickle.loads(pCity.getScriptData())
	#if (sBuilding == 'BUILDING_CRAFTSMEN_GUILD' and strCheckData['BUILDING_CRAFTSMEN_GUILD'] > CyGame().getGameTurn()):
	#	return False
	#if (sBuilding == 'BUILDING_HERBALIST' and strCheckData['BUILDING_HERBALIST'] > CyGame().getGameTurn()):
	#	return False
	# if (sBuilding == 'BUILDING_ALCHEMY_LAB' and strCheckData['BUILDING_ALCHEMY_LAB'] > CyGame().getGameTurn()):
		# return False
	# if (sBuilding == 'BUILDING_MAGE_GUILD' and strCheckData['BUILDING_MAGE_GUILD'] > CyGame().getGameTurn()):
		# return False
	# if (sBuilding == 'BUILDING_LIBRARY' and strCheckData['BUILDING_LIBRARY'] > CyGame().getGameTurn()):
		# return False

	return True

def reqBecomeChief(caster):
	iChief = gc.getInfoTypeForString('PROMOTION_CHIEF')
	
	if not reqBuilding(caster,'BUILDING_ELDER_COUNCIL','PROMOTION_CHIEF'):
		return False
	if caster.getLevel() < 5:
		return False
	if caster.isHasPromotion(iChief):
		return False

	iClassUnits = 0
	iChiefUnits = 0
	SearchClass = caster.getUnitClassType()
	py = PyPlayer(caster.getOwner())
	for pUnit in py.getUnitList():
		if pUnit.getUnitClassType() == SearchClass:
			iClassUnits += 1
			if pUnit.isHasPromotion(iChief):
				iChiefUnits += 1
	if iChiefUnits < iClassUnits / 10 + 1:
		return True

	return False
	
def reqBecomeGrandMaster(caster):
	if caster.getLevel() < 6:
		return False
	#if caster.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_HIDDEN_CACHE'):
	#	return False
	iGrandMaster = gc.getInfoTypeForString('PROMOTION_GRAND_MASTER')
	if caster.isHasPromotion(iGrandMaster):
		return False
	iCount = 0

	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			py = PyPlayer(iPlayer)
			for pUnit in py.getUnitList():
				if pUnit.getUnitClassType() == caster.getUnitClassType():
					iCount = iCount + 1
					if pUnit.isHasPromotion(iGrandMaster):
						if caster.getLevel() <= pUnit.getLevel():
							return False

	if iCount < 12:
		return False

	return True
	
def spellBecomeGrandMaster(caster):
	iGrandMaster = gc.getInfoTypeForString('PROMOTION_GRAND_MASTER')
	destPlayer = gc.getPlayer(caster.getOwner())
	sMsg = 'A ' + caster.getName() + ' in the service of ' + destPlayer.getName() + ' claims the title of grand master!'
	for iPlayer in range(gc.getMAX_PLAYERS()):
		pPlayer = gc.getPlayer(iPlayer)
		if pPlayer.isAlive():
			py = PyPlayer(iPlayer)
			CyInterface().addMessage(iPlayer,true,25,sMsg,'',1,'Art/Interface/Buttons/Spells/Banish.dds',ColorTypes(8),caster.getX(),caster.getY(),True,True)
			for pUnit in py.getUnitList():
				if (pUnit.isHasPromotion(iGrandMaster) and pUnit.getUnitClassType() == caster.getUnitClassType()):
					pUnit.setHasPromotion(iGrandMaster, False)

	caster.setHasPromotion(iGrandMaster, True)
	
def reqCommandMorale(caster):
	if not (caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDER1')) or caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHIEF')) or caster.getUnitType() == gc.getInfoTypeForString('UNIT_MARDERO')):
		return False
	if cf.getObjectInt(caster,'Command') == CyGame().getGameTurn():
		return False
	iBlessAll = 1
	if not caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDER1')):
		iBlessAll = 0
	UnitType = caster.getUnitType()
	if caster.getUnitType() == gc.getInfoTypeForString('UNIT_MARDERO'):
		UnitType = gc.getInfoTypeForString('UNIT_SUCCUBUS')

	iNumBlessed = caster.getLevel()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDER2')):
		iNumBlessed = iNumBlessed + caster.getLevel()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDER3')):
		iNumBlessed = iNumBlessed + caster.getLevel()
	iRange = iNumBlessed / 8

	for iiX in range(caster.getX()-iRange, caster.getX()+iRange+1, 1):
		for iiY in range(caster.getY()-iRange, caster.getY()+iRange+1, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if (pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMAND_MORALE')) == False and pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHIEF')) == False and caster.getTeam() == pUnit.getTeam()):
					if (pUnit.getUnitType() == UnitType or iBlessAll == 1):
						return True
	return False

def spellCommandMorale(caster):
	cf.setObjectInt(caster,'Command',CyGame().getGameTurn())

	iNumBlessed=caster.getLevel()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDER2')):
		iNumBlessed = iNumBlessed + caster.getLevel()
	if caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDER3')):
		iNumBlessed = iNumBlessed + caster.getLevel()
	iRange = iNumBlessed / 8

	iBlessAll = 1
	if not caster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMANDER1')):
		iBlessAll = 0
	UnitType = caster.getUnitType()
	if caster.getUnitType() == gc.getInfoTypeForString('UNIT_MARDERO'):
		UnitType = gc.getInfoTypeForString('UNIT_SUCCUBUS')

	pPlot = caster.plot()
	for i in range(pPlot.getNumUnits()):
		pUnit = pPlot.getUnit(i)
		if not (pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMAND_MORALE'))):
			if (iBlessAll == 1 or UnitType == pUnit.getUnitType()):
				pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMAND_MORALE'),True)
				iNumBlessed = iNumBlessed - 1
				if (iNumBlessed < 1):
					return

	for iiX in range(caster.getX()-iRange, caster.getX()+iRange+1, 1):
		for iiY in range(caster.getY()-iRange, caster.getY()+iRange+1, 1):
			pPlot = CyMap().plot(iiX,iiY)
			for i in range(pPlot.getNumUnits()):
				pUnit = pPlot.getUnit(i)
				if not pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMAND_MORALE')) and caster.getTeam() == pUnit.getTeam():
					if (iBlessAll == 1 or UnitType == pUnit.getUnitType()):
						pUnit.setHasPromotion(gc.getInfoTypeForString('PROMOTION_COMMAND_MORALE'),True)
						iNumBlessed = iNumBlessed - 1
						if (iNumBlessed < 1):
							return


