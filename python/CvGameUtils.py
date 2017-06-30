## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Implementaion of miscellaneous game functions

import CvUtil
from CvPythonExtensions import *
import CvEventInterface
import CustomFunctions
import ScenarioFunctions
import cPickle
import math

import PyHelpers
PyPlayer = PyHelpers.PyPlayer

# globals
cf = CustomFunctions.CustomFunctions()
gc = CyGlobalContext()
sf = ScenarioFunctions.ScenarioFunctions()



class CvGameUtils:
	"Miscellaneous game functions"
	def __init__(self): 
		pass
	
	def isVictoryTest(self):
		if ( gc.getGame().getElapsedGameTurns() > 10 ):
			return True
		else:
			return False

	def isVictory(self, argsList):
		eVictory = argsList[0]
		return True

	def isPlayerResearch(self, argsList):
		ePlayer = argsList[0]
		return True

	def getExtraCost(self, argsList):
		ePlayer = argsList[0]
		return 0

	def createBarbarianCities(self):
		return False
		
	def createBarbarianUnits(self):
		return False
		
	def skipResearchPopup(self,argsList):
		ePlayer = argsList[0]
		return False
		
	def showTechChooserButton(self,argsList):
		ePlayer = argsList[0]
		return True

	def getFirstRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		return TechTypes.NO_TECH

	def getSecondRecommendedTech(self,argsList):
		ePlayer = argsList[0]
		eFirstTech = argsList[1]
		return TechTypes.NO_TECH
	
	def canRazeCity(self,argsList):
		iRazingPlayer, pCity = argsList
		return True
	
	def canDeclareWar(self,argsList):
		iAttackingTeam, iDefendingTeam = argsList
		return True
	
	def skipProductionPopup(self,argsList):
		pCity = argsList[0]
		return False
		
	def showExamineCityButton(self,argsList):
		pCity = argsList[0]
		return True

	def getRecommendedUnit(self,argsList):
		pCity = argsList[0]
		return UnitTypes.NO_UNIT

	def getRecommendedBuilding(self,argsList):
		pCity = argsList[0]
		return BuildingTypes.NO_BUILDING

	def updateColoredPlots(self):
		return False

	def isActionRecommended(self,argsList):
		pUnit = argsList[0]
		iAction = argsList[1]
		return False

	def unitCannotMoveInto(self,argsList):
		ePlayer = argsList[0]		
		iUnitId = argsList[1]
		iPlotX = argsList[2]
		iPlotY = argsList[3]
		return False

	def cannotHandleAction(self,argsList):
		pPlot = argsList[0]
		iAction = argsList[1]
		bTestVisible = argsList[2]
		return False

	def canBuild(self,argsList):
		iX, iY, iBuild, iPlayer = argsList
		pPlayer = gc.getPlayer(iPlayer)
		eTeam = gc.getTeam(pPlayer.getTeam())

		if pPlayer.isHuman() == False:
			pPlot = CyMap().plot(iX, iY)
			iterrain=pPlot.getTerrainType()
			if iBuild == gc.getInfoTypeForString('BUILD_FORT'):
				return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WINDMILL'):
				if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_LABOR')) == gc.getInfoTypeForString('CIVIC_ARETE'):
					return 0
			if iBuild == gc.getInfoTypeForString('BUILD_WORKSHOP'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_GUILDS')) == False :
					if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')) :
						return 0
			if iBuild == gc.getInfoTypeForString('BUILD_COTTAGE'):
				if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_GOVERNMENT')) == gc.getInfoTypeForString('CIVIC_ARISTOCRACY'):
					return 0
#				if iterrain!=gc.getInfoTypeForString('TERRAIN_PLAINS'):
#					if pPlot.canBuild(gc.getInfoTypeForString('BUILD_FARM'),iPlayer,False):
#						return 0
			if iBuild == gc.getInfoTypeForString('BUILD_FARM'):
				if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FALLOW')):
					return 0				
					
			if iBuild==gc.getInfoTypeForString('BUILD_ROAD'):
				if pPlot.isWater():
					return 0

		return -1	# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can

	def cannotFoundCity(self,argsList):
		iPlayer, iPlotX, iPlotY = argsList
		pPlot = CyMap().plot(iPlotX,iPlotY)
		return False

	def cannotSelectionListMove(self,argsList):
		pPlot = argsList[0]
		bAlt = argsList[1]
		bShift = argsList[2]
		bCtrl = argsList[3]
		return False

	def cannotSelectionListGameNetMessage(self,argsList):
		eMessage = argsList[0]
		iData2 = argsList[1]
		iData3 = argsList[2]
		iData4 = argsList[3]
		iFlags = argsList[4]
		bAlt = argsList[5]
		bShift = argsList[6]
		return False

	def cannotDoControl(self,argsList):
		eControl = argsList[0]
		return False

	def canResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		return False

	def cannotResearch(self,argsList):
		ePlayer = argsList[0]
		eTech = argsList[1]
		bTrade = argsList[2]
		pPlayer = gc.getPlayer(ePlayer)
		iCiv = pPlayer.getCivilizationType()
		eTeam = gc.getTeam(pPlayer.getTeam())
		
		if eTech == gc.getInfoTypeForString('TECH_ORDERS_FROM_HEAVEN'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_1):
				return True
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):
				return True
			if pPlayer.isHuman() == False:
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getReligionWeightModifier(gc.getInfoTypeForString('RELIGION_THE_ORDER'))<0:
					return True
		if eTech == gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_3):
				return True
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):
				return True
			if pPlayer.isHuman() == False:
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getReligionWeightModifier(gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'))<0:
					return True
				
		if eTech == gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_0):
				return True
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):
				return True
			if pPlayer.isHuman() == False:
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getReligionWeightModifier(gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'))<0:
					return True
				
		if eTech == gc.getInfoTypeForString('TECH_MESSAGE_FROM_THE_DEEP'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_2):
				return True
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):
				return True
			if pPlayer.isHuman() == False:
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getReligionWeightModifier(gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'))<0:
					return True
				
		if eTech == gc.getInfoTypeForString('TECH_CORRUPTION_OF_SPIRIT'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_RELIGION_4):
				return True
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):
				return True
			if pPlayer.isHuman() == False:
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getReligionWeightModifier(gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'))<0:
					return True
				
		if eTech == gc.getInfoTypeForString('TECH_HONOR'):
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):
				return True		
			if pPlayer.isHuman() == False:
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getReligionWeightModifier(gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'))<0:
					return True
				
		if eTech == gc.getInfoTypeForString('TECH_DECEPTION'):
			if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):
				return True		
			if pPlayer.isHuman() == False:
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getReligionWeightModifier(gc.getInfoTypeForString('RELIGION_COUNCIL_OF_ESUS'))<0:
					return True

		if eTech == gc.getInfoTypeForString('TECH_SEAFARING'):
			if iCiv != gc.getInfoTypeForString('CIVILIZATION_LANUN'):
				return True
		if pPlayer.isHuman() == False:
			if eTech == gc.getInfoTypeForString('TECH_STIRRUPS'):
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
					return True
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
					return True
										
		if CyGame().getWBMapScript():
			bBlock = sf.cannotResearch(ePlayer, eTech, bTrade)
			if bBlock:
				return True

		return False

	def canDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		return False

	def cannotDoCivic(self,argsList):
		ePlayer = argsList[0]
		eCivic = argsList[1]
		pPlayer = gc.getPlayer(ePlayer)
		eTeam = gc.getTeam(pPlayer.getTeam())

		return False
		
	def canTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		return False

	def cannotTrain(self,argsList):
		pCity = argsList[0]
		eUnit = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		bIgnoreUpgrades = argsList[5]
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		eUnitClass = gc.getUnitInfo(eUnit).getUnitClassType()
		eTeam = gc.getTeam(pPlayer.getTeam())

		sCityInfo = { 'OBELISK': 1, 'TEMPLE': 1 }
		if pPlayer.isHuman() or pCity.getPopulation() > 1:
			try:
				sCityInfo =cPickle.loads(pCity.getScriptData())
			except EOFError:
				sCityInfo = { 'OBELISK': 1, 'TEMPLE': 1 }

		if pPlayer.isHuman() == False:
			infoCiv = gc.getCivilizationInfo(pPlayer.getCivilizationType())
			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_SCOUT'):
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_SCOUT')) >= 1:
					return True
				iHuntingLodge = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))
				if iHuntingLodge != -1:
					if pPlayer.canConstruct(iHuntingLodge, False, False, False):
						return True
			if eUnit == gc.getInfoTypeForString('UNIT_DEMAGOG'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DEMAGOG')) > 6:
					return True
			if eUnit == gc.getInfoTypeForString('UNIT_SETTLER'):		
				if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
					if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_SETTLER')) > 0:
						if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FESTIVALS')) == False:
							return True
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_SETTLER')) > 1:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FESTIVALS')) == False:
						return True

			if eUnit == gc.getInfoTypeForString('UNIT_WORKER'):
				if pPlayer.getNumCities() + 2 <= pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_WORKER')):
					return True

			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_WARRIOR'):
				civtype = pPlayer.getCivilizationType()
				infoCiv = gc.getCivilizationInfo(civtype)			
				iUnit = infoCiv.getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_AXEMAN'))
				if iUnit != -1:
					if pCity.canTrain(iUnit,False,False):
						return True
				iUnit = infoCiv.getCivilizationUnits(gc.getInfoTypeForString('UNITCLASS_ARCHER'))
				if iUnit != -1:
					if pCity.canTrain(iUnit,False,False):
						return True

			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_ADEPT'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT')) > 3+pPlayer.getNumCities()*2:
					if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_ARCANE')) :
						if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):
							return True
					elif not pPlayer.isConquestMode():
						return True
			if eUnit == gc.getInfoTypeForString('UNIT_AIRSHIP'):
				return True
			if eUnit == gc.getInfoTypeForString('UNIT_LIGHTBRINGER'):
				return True
			if eUnit == gc.getInfoTypeForString('UNIT_DWARVEN_SOLDIER_RUNES'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DWARVEN_SOLDIER_RUNES')) > 2:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')): 
						return True
			if eUnit == gc.getInfoTypeForString('UNIT_DROWN'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_DROWN')) > 2:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')): 
						return True
			if eUnit == gc.getInfoTypeForString('UNIT_FAWN'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_FAWN')) > 2:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')): 
						return True	
			if eUnit == gc.getInfoTypeForString('UNIT_CRUSADER'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CRUSADER')) > 2:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')): 
						return True	
			if eUnit == gc.getInfoTypeForString('UNIT_PARAMANDER'):
				if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PARAMANDER')) > 2:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')): 
						return True	

			if eUnitClass == gc.getInfoTypeForString('UNITCLASS_LOKI'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FESTIVALS')) == False:
					return True

			if eUnit == gc.getInfoTypeForString('UNIT_PRIVATEER'):
				iPrivateercounter = 0
				for iTeam2 in range(gc.getMAX_PLAYERS()):
					eTeam2 = gc.getTeam(iTeam2)
					if eTeam2.isAlive():
						if eTeam2.isHasTech(gc.getInfoTypeForString('TECH_OPTICS')) and eTeam2.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
							iPrivateercounter = iPrivateercounter +1
				if iPrivateercounter > 1:
					return True
          
		if eUnit == gc.getInfoTypeForString('UNIT_PRIEST_OF_KILMORPH'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_KILMORPH')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')) / 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_KILMORPH')):
					return True
				
		if eUnit == gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_ORDER'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_ORDER')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')) / 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_ORDER')):
					return True
		
		if eUnit == gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_LEAVES')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES')) / 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_LEAVES')):
					return True
				
		if eUnit == gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_EMPYREAN'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_EMPYREAN')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')) / 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_EMPYREAN')):
					return True
				
		if eUnit == gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_OVERLORDS'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_OVERLORDS')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')) / 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_OVERLORDS')):
					return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_PRIEST_OF_THE_VEIL'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_VEIL')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')) / 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_VEIL')):
					return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_KILMORPH'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_KILMORPH')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH')) / 7 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_KILMORPH')):
					return True
				
		if eUnit == gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_THE_ORDER'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_ORDER')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER')) / 7 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_ORDER')):
					return True
		
		if eUnit == gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_LEAVES'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_LEAVES')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES')) / 7 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_LEAVES')):
					return True
				
		if eUnit == gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_THE_EMPYREAN'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_EMPYREAN')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN')) / 7 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_EMPYREAN')):
					return True
				
		if eUnit == gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_THE_OVERLORDS'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_OVERLORDS')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS')) / 7 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_OVERLORDS')):
					return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_HIGH_PRIEST_OF_THE_VEIL'):
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_VEIL')):
					return True
			else:
				if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL')) / 7 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_VEIL')):
					return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_MERCHANT_SHIP'):
			if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_HARBOR')) + pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_HARBOR_LANUN')) <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MERCHANT_SHIP')):
				return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_MAGE'):
			if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_MAGE_GUILD')) * 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE')):
				return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_ILLUSIONIST'):
			if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_MAGE_GUILD')) * 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ILLUSIONIST')):
				return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_WIZARD'):
			if pPlayer.countNumBuildings(gc.getInfoTypeForString('BUILDING_MAGE_GUILD')) * 3 <= pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_WIZARD')):
				return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_BEAST_OF_AGARES'):
			if pCity.getPopulation() <= 5:
				return True

		if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) == gc.getInfoTypeForString('CIVIC_CRUSADE'):
			if eUnit == gc.getInfoTypeForString('UNIT_WORKER'):
				return True
			if eUnit == gc.getInfoTypeForString('UNIT_SETTLER'):
				return True
			if eUnit == gc.getInfoTypeForString('UNIT_WORKBOAT'):
				return True

		if eUnit == gc.getInfoTypeForString('UNIT_ACHERON'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_ACHERON):
				return True

		if eUnit == gc.getInfoTypeForString('UNIT_DUIN'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_DUIN):
				return True		
								
		if CyGame().getWBMapScript():
			bBlock = sf.cannotTrain(pCity, eUnit, bContinue, bTestVisible, bIgnoreCost, bIgnoreUpgrades)
			if bBlock:
				return True

		if eUnit == gc.getInfoTypeForString('UNIT_GRIFFON'):
			if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TOWER_OF_DIVINATION')) == 0:
				return True
					
		if eUnit == gc.getInfoTypeForString('UNIT_MAGICIAN'):
			if 'OBELISK' not in sCityInfo:
				sCityInfo['OBELISK'] = 1
			if sCityInfo['OBELISK'] > 0 or pCity.getCulture(pCity.getOwner()) < 1000:
				return True

		if eUnit == gc.getInfoTypeForString('UNIT_PRIEST'):
			if 'TEMPLE' not in sCityInfo:
				sCityInfo['TEMPLE'] = 1
			if sCityInfo['TEMPLE'] > 0 or pCity.getCulture(pCity.getOwner()) < 1000:
				return True

		if eUnit == gc.getInfoTypeForString('UNIT_RECRUIT'):
			if CyGame().getGameTurn() > 0:
				return True

		return False

	def canConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		return False

	def cannotConstruct(self,argsList):
		pCity = argsList[0]
		eBuilding = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		bIgnoreCost = argsList[4]
		pPlayer = gc.getPlayer(pCity.getOwner())
		iBuildingClass = gc.getBuildingInfo(eBuilding).getBuildingClassType()
		eTeam = gc.getTeam(pPlayer.getTeam())
		pPlot = pCity.plot()
		iAreaSize = pPlot.area().getNumTiles()
				
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):		
			if eBuilding == gc.getInfoTypeForString('BUILDING_TEMPLE_OF_LEAVES'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_TEMPLE_OF_KILMORPH'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_EMPYREAN'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_OVERLORDS'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_VEIL'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_TEMPLE_OF_THE_ORDER'):
				return True								
		
		if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) == gc.getInfoTypeForString('CIVIC_CRUSADE'):
			if eBuilding == gc.getInfoTypeForString('BUILDING_ELDER_COUNCIL'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_MARKET'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_MONUMENT'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_MONEYCHANGER'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_THEATRE'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_AQUEDUCT'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_PUBLIC_BATHS'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_HERBALIST'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_CARNIVAL'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_COURTHOUSE'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_GRANARY'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_SMOKEHOUSE'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_LIBRARY'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_HARBOR'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_ALCHEMY_LAB'):
				return True
			if eBuilding == gc.getInfoTypeForString('BUILDING_BREWERY'):
				return True

		if eBuilding == gc.getInfoTypeForString('BUILDING_DEEPER_MINES_OF_GALDUR'):
			if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_MINES_OF_GALDUR')) == 0:
				return True

		if eBuilding == gc.getInfoTypeForString('BUILDING_MINES_OF_GALDUR_DEPTHS'):
			if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_DEEPER_MINES_OF_GALDUR')) == 0:
				return True

		if eBuilding == gc.getInfoTypeForString('BUILDING_ISLAND_RESORT'):
			if iAreaSize > 7:
				return True

		if eBuilding == gc.getInfoTypeForString('BUILDING_SHRINE_OF_THE_CHAMPION'):
			iHero = cf.getHero(pPlayer)
			if iHero == -1:
				return True
			if CyGame().isUnitClassMaxedOut(iHero, 0) == False:
				return True
			if pPlayer.getUnitClassCount(iHero) > 0:
				return True

		if eBuilding == gc.getInfoTypeForString('BUILDING_MERCURIAN_GATE'):
			if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_HYBOREM_OR_BASIUM):
				return True
			if pPlayer.getStateReligion() == gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				return True
			if pCity.isCapital():
				return True
			if not cf.bTechExist('TECH_INFERNAL_PACT'):
				return True
			if pPlayer.isHuman() == False:
				if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
					return True

		iAltar1 = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR')
		iAltar2 = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_ANOINTED')
		iAltar3 = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_BLESSED')
		iAltar4 = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_CONSECRATED')
		iAltar5 = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_DIVINE')
		iAltar6 = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_EXALTED')
		iAltar7 = gc.getInfoTypeForString('BUILDING_ALTAR_OF_THE_LUONNOTAR_FINAL')
		if (eBuilding == iAltar1 or eBuilding == iAltar2 or eBuilding == iAltar3 or eBuilding == iAltar4 or eBuilding == iAltar5 or eBuilding == iAltar6 or eBuilding == iAltar7):
			if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
				return True
			if eBuilding == iAltar1:
				if (pPlayer.countNumBuildings(iAltar2) > 0 or pPlayer.countNumBuildings(iAltar3) > 0 or pPlayer.countNumBuildings(iAltar4) > 0 or pPlayer.countNumBuildings(iAltar5) > 0 or pPlayer.countNumBuildings(iAltar6) > 0 or pPlayer.countNumBuildings(iAltar7) > 0):
					return True
			if eBuilding == iAltar2:
				if (pPlayer.countNumBuildings(iAltar3) > 0 or pPlayer.countNumBuildings(iAltar4) > 0 or pPlayer.countNumBuildings(iAltar5) > 0 or pPlayer.countNumBuildings(iAltar6) > 0 or pPlayer.countNumBuildings(iAltar7) > 0):
					return True
			if eBuilding == iAltar3:
				if (pPlayer.countNumBuildings(iAltar4) > 0 or pPlayer.countNumBuildings(iAltar5) > 0 or pPlayer.countNumBuildings(iAltar6) > 0 or pPlayer.countNumBuildings(iAltar7) > 0):
					return True
			if eBuilding == iAltar4:
				if (pPlayer.countNumBuildings(iAltar5) > 0 or pPlayer.countNumBuildings(iAltar6) > 0 or pPlayer.countNumBuildings(iAltar7) > 0):
					return True
			if eBuilding == iAltar5:
				if (pPlayer.countNumBuildings(iAltar6) > 0 or pPlayer.countNumBuildings(iAltar7) > 0):
					return True
			if eBuilding == iAltar6:
				if pPlayer.countNumBuildings(iAltar7) > 0:
					return True

		if pPlayer.isHuman() == False:
			if eBuilding == gc.getInfoTypeForString('BUILDING_PROPHECY_OF_RAGNAROK'):
				if pPlayer.getAlignment() != gc.getInfoTypeForString('ALIGNMENT_EVIL'):
					return True

		if eBuilding == gc.getInfoTypeForString('BUILDING_SMUGGLERS_PORT'):
			if pPlayer.isSmugglingRing() == False:
				return True

		return False

	def canCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		return False

	def cannotCreate(self,argsList):
		pCity = argsList[0]
		eProject = argsList[1]
		bContinue = argsList[2]
		bTestVisible = argsList[3]
		pPlayer = gc.getPlayer(pCity.getOwner())
		eTeam = gc.getTeam(pPlayer.getTeam())
		
		if eProject == gc.getInfoTypeForString('PROJECT_PURGE_THE_UNFAITHFUL'):
			if pPlayer.isHuman() == False:
				return True
			if pPlayer.getStateReligion() == -1:
				return True

		if eProject == gc.getInfoTypeForString('PROJECT_BIRTHRIGHT_REGAINED'):
			if not pPlayer.isFeatAccomplished(FeatTypes.FEAT_GLOBAL_SPELL):
				return True

		if eProject == gc.getInfoTypeForString('PROJECT_STIR_FROM_SLUMBER'):
			if pPlayer.getPlayersKilled() == 0:
				return True

		if eProject == gc.getInfoTypeForString('PROJECT_GENESIS'):
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
				return True
		
		if eProject == gc.getInfoTypeForString('PROJECT_SAMHAIN'):						
			if pPlayer.isHuman() == False:		
				if pPlayer.getNumCities() <= 3:
					return True
		
		if pPlayer.isHuman() == False:
			if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_WARRIOR')) <= 2:
				if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
					if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_ARCHERY')):
						return True
			if pCity.getBaseYieldRate(1) <= 10:
				return True
		
		return False

	def canMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False

	def cannotMaintain(self,argsList):
		pCity = argsList[0]
		eProcess = argsList[1]
		bContinue = argsList[2]
		return False   

	def AI_chooseTech(self,argsList):
		ePlayer = argsList[0]
		bFree = argsList[1]
		pPlayer = gc.getPlayer(ePlayer)
		pCity = pPlayer.getCapitalCity()
		iCiv=pPlayer.getCivilizationType()
		iFavRel=pPlayer.getFavoriteReligion()
		eTeam = gc.getTeam(pPlayer.getTeam())
		iTech = -1
		
		bTier2 = false
		bTier3 = false
		bTier4 = false
		bEcon1 = false
		bEcon2 = false
		bEcon3 = false


		
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):		
			bTier2 = True
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ARCHERY')):		
			bTier2 = True
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):		
			bTier2 = True
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')):		
			bTier2 = True
		if iCiv == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')):				
				bTier2 = True	

		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):		
			bTier3 = True
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BOWYERS')):		
			bTier3 = True
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_STIRRUPS')):		
			bTier3 = True
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HANDLING')):		
			bTier3 = True

		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MINING')):		
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CALENDAR')):		
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_EDUCATION')):		
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_EXPLORATION')):						
						bEcon1 = True
		CountEcontechs=0
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_TRADE')):		
			CountEcontechs=CountEcontechs+1
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SANITATION')):		
			CountEcontechs=CountEcontechs+1
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):		
			CountEcontechs=CountEcontechs+1		
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')):						
			CountEcontechs=CountEcontechs+1	
		if eTeam.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):						
			CountEcontechs=CountEcontechs+1				
		econval=gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getEconomyTechValue()
		if econval>130:
			econval=130
		if (((CountEcontechs*95)+150)>(4*econval)):
			bEcon2 = True

			
		if (bTier3 and bEcon2): 

			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):
				counttowers=0
				if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_ALTERATION'))>0:
					counttowers=counttowers+1
				if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_DIVINATION'))>0:						
					counttowers=counttowers+1				
				if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'))>0:			
					counttowers=counttowers+1				
				if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS'))>0:							
					counttowers=counttowers+1
				if counttowers>2:
					return gc.getInfoTypeForString('TECH_STRENGTH_OF_WILL')
			
#Altar Victory
			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isAltarVictory():
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_RELIGIOUS_LAW')):
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_OMNISCIENCE')) == False:
						iTech = gc.getInfoTypeForString('TECH_OMNISCIENCE')

				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_RELIGIOUS_LAW')) == False:
					iTech = gc.getInfoTypeForString('TECH_RELIGIOUS_LAW')

			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isCultureVictory():
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MERCANTILISM')) == False:
					iTech = gc.getInfoTypeForString('TECH_MERCANTILISM')
#Magic Techs
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ALTERATION')) == False:
				iTech = gc.getInfoTypeForString('TECH_ALTERATION')			

			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_DIVINATION')) == False:
				iTech = gc.getInfoTypeForString('TECH_DIVINATION')
				
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ELEMENTALISM')) == False:
				iTech = gc.getInfoTypeForString('TECH_ELEMENTALISM')

			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_NECROMANCY')) == False:
				iTech = gc.getInfoTypeForString('TECH_NECROMANCY')

# Late Wonder Beeline		
			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteLateWonder()!=BuildingClassTypes.NO_BUILDINGCLASS:
				temp=gc.getCivilizationInfo(iCiv).getCivilizationBuildings(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteLateWonder())			
				newtech=gc.getBuildingInfo(temp).getPrereqAndTech()
				if newtech!=TechTypes.NO_TECH:
					if eTeam.isHasTech(newtech) == False:
						if pPlayer.canResearch(newtech,False):																
							iTech = newtech
				
# Religion Heroes Beeline						
			if (iFavRel !=ReligionTypes.NO_RELIGION):
				if (gc.getReligionInfo(iFavRel).getReligionHero2()!=UnitClassTypes.NO_UNITCLASS):						
					tUnit = gc.getUnitClassInfo(gc.getReligionInfo(iFavRel).getReligionHero2()).getDefaultUnitIndex()
					if (gc.getUnitInfo(tUnit).getPrereqAndTech()!=TechTypes.NO_TECH):
						if eTeam.isHasTech(gc.getUnitInfo(tUnit).getPrereqAndTech()) ==False:
							if pPlayer.canResearch(gc.getUnitInfo(tUnit).getPrereqAndTech(),False):											
								iTech = gc.getUnitInfo(tUnit).getPrereqAndTech()
		
			if (iFavRel !=ReligionTypes.NO_RELIGION):
				if (gc.getReligionInfo(iFavRel).getReligionHero1()!=UnitClassTypes.NO_UNITCLASS):			
					tUnit = gc.getUnitClassInfo(gc.getReligionInfo(iFavRel).getReligionHero1()).getDefaultUnitIndex()
					if (gc.getUnitInfo(tUnit).getPrereqAndTech()!=TechTypes.NO_TECH):					
						if eTeam.isHasTech(gc.getUnitInfo(tUnit).getPrereqAndTech()) ==False:
							if pPlayer.canResearch(gc.getUnitInfo(tUnit).getPrereqAndTech(),False):											
								iTech = gc.getUnitInfo(tUnit).getPrereqAndTech()

			if iFavRel!=ReligionTypes.NO_RELIGION:
				if iFavRel== gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
					if pPlayer.canResearch(gc.getInfoTypeForString('TECH_PRIESTHOOD'),False):																				
						iTech = gc.getInfoTypeForString('TECH_PRIESTHOOD')

#Advanced Economic techs in case we haven't picked them up yet								
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):		
				iTech = gc.getInfoTypeForString('TECH_TAXATION')				
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):		
				iTech = gc.getInfoTypeForString('TECH_CURRENCY')							
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')):		
				iTech = gc.getInfoTypeForString('TECH_CONSTRUCTION')
				
#resource techs
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_HUNTING')):		
				iTech = gc.getInfoTypeForString('TECH_HUNTING')
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY')):		
				iTech = gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY')
								
				
#more advanced beelines
		if (bTier2 and bEcon2):		
						
#Civ Specific 		
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')) == False:
					iTech = gc.getInfoTypeForString('TECH_SORCERY')						
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BOWYERS')) == False:
					iTech = gc.getInfoTypeForString('TECH_BOWYERS')			

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) == False:
					iTech = gc.getInfoTypeForString('TECH_IRON_WORKING')			

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_BANNOR'):	
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FANATICISM')) == False:
					iTech = gc.getInfoTypeForString('TECH_FANATICISM')													
	
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):	
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FEUDALISM')) == False:
					iTech = gc.getInfoTypeForString('TECH_FEUDALISM')													

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) == False:
					iTech = gc.getInfoTypeForString('TECH_IRON_WORKING')								
	
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) == False:
					iTech = gc.getInfoTypeForString('TECH_IRON_WORKING')			

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD')) == False:
					iTech = gc.getInfoTypeForString('TECH_PRIESTHOOD')
					
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) == False:
					iTech = gc.getInfoTypeForString('TECH_IRON_WORKING')								
				elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_MEDICINE')) == False:
					iTech = gc.getInfoTypeForString('TECH_MEDICINE')								

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_STIRRUPS')) == False:
					iTech = gc.getInfoTypeForString('TECH_STIRRUPS')													

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) == False:
					iTech = gc.getInfoTypeForString('TECH_IRON_WORKING')			
						
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_TRADE')) :
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ELEMENTALISM')) == False:	
						iTech = gc.getInfoTypeForString('TECH_ELEMENTALISM')	
					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')) == False:
						iTech = gc.getInfoTypeForString('TECH_SORCERY')
#					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_MACHINERY')) == False:
#						if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BOWYERS')):
#							iTech = gc.getInfoTypeForString('TECH_MACHINERY')
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) == False:
						iTech = gc.getInfoTypeForString('TECH_IRON_WORKING')								

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_STIRRUPS')) == False:
					iTech = gc.getInfoTypeForString('TECH_STIRRUPS')													

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')) == False:
					iTech = gc.getInfoTypeForString('TECH_IRON_WORKING')								

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BOWYERS')) == False:
					iTech = gc.getInfoTypeForString('TECH_BOWYERS')								

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_PRIESTHOOD')) == False:
					iTech = gc.getInfoTypeForString('TECH_PRIESTHOOD')

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')) == False:
					iTech = gc.getInfoTypeForString('TECH_SORCERY')									
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_NECROMANCY')) == False:
					iTech = gc.getInfoTypeForString('TECH_NECROMANCY')						
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CORRUPTION_OF_SPIRIT')) == False:
					iTech = gc.getInfoTypeForString('TECH_CORRUPTION_OF_SPIRIT')			

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_POISONS')) == False:
					iTech = gc.getInfoTypeForString('TECH_POISONS')																
				elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HANDLING')) == False:
					iTech = gc.getInfoTypeForString('TECH_ANIMAL_HANDLING')

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_POISONS')) == False:
					iTech = gc.getInfoTypeForString('TECH_POISONS')																
				elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HANDLING')) == False:
					iTech = gc.getInfoTypeForString('TECH_ANIMAL_HANDLING')
						
#Advanced Religion Beelines					
							
			if (iFavRel !=ReligionTypes.NO_RELIGION):
				if (gc.getReligionInfo(iFavRel).getReligionTech2()!=TechTypes.NO_TECH):										
					if eTeam.isHasTech(gc.getReligionInfo(iFavRel).getReligionTech2()) == False:
						if pPlayer.canResearch(gc.getReligionInfo(iFavRel).getReligionTech2(),False):
							iTech = gc.getReligionInfo(iFavRel).getReligionTech2()			
				if (gc.getReligionInfo(iFavRel).getReligionTech1()!=TechTypes.NO_TECH):			
					if eTeam.isHasTech(gc.getReligionInfo(iFavRel).getReligionTech1()) == False:
						if pPlayer.canResearch(gc.getReligionInfo(iFavRel).getReligionTech1(),False):					
							iTech = gc.getReligionInfo(iFavRel).getReligionTech1()

							
#----------------------------			
#Establish a Good Economy
#----------------------------						

		if (bTier2 and not bEcon2):
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_TAXATION')):
				iTech = gc.getInfoTypeForString('TECH_TAXATION')
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_CURRENCY')):
				iTech = gc.getInfoTypeForString('TECH_CURRENCY')
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')):
				iTech = gc.getInfoTypeForString('TECH_CONSTRUCTION')
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_SANITATION')):		
				iTech = gc.getInfoTypeForString('TECH_SANITATION')							
			if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_TRADE')):		
				iTech = gc.getInfoTypeForString('TECH_TRADE')							
									
					
#----------------------------			
#Teching with early economy and military
#----------------------------
		if (bTier2 and bEcon1):	

# Early Wonder Beeline		
			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyWonder()!=BuildingClassTypes.NO_BUILDINGCLASS:
				temp=gc.getCivilizationInfo(iCiv).getCivilizationBuildings(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyWonder())			
				newtech=gc.getBuildingInfo(temp).getPrereqAndTech()
				if newtech!=TechTypes.NO_TECH:				
					if eTeam.isHasTech(newtech) == False:
						if pPlayer.canResearch(iTech,False):																				
							iTech = newtech
				
#Early Leader Beelines
			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech3()!=TechTypes.NO_TECH:
				if eTeam.isHasTech(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech3()) == False:
					if pPlayer.canResearch(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech3(),False):
						iTech = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech3()

			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech2()!=TechTypes.NO_TECH:
				if eTeam.isHasTech(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech2()) == False:
					if pPlayer.canResearch(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech2(),False):
						iTech = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech2()

			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech1()!=TechTypes.NO_TECH:
				if eTeam.isHasTech(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech1()) == False:
					if pPlayer.canResearch(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech1(),False):
						iTech = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyTech1()
					
#Early Civ Beelines			
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_EDUCATION')): 
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CODE_OF_LAWS')) == False:
						iTech = gc.getInfoTypeForString('TECH_CODE_OF_LAWS')

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
				if pPlayer.getNumCities() >=3:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MASONRY')) == False:
						iTech = gc.getInfoTypeForString('TECH_MASONRY')
						
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_EDUCATION')) :
					if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')) :		
						iTech = gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')
					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_IRON_WORKING')):
						if bEcon2:
							if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_WARHORSES')):
								iTech = gc.getInfoTypeForString('TECH_WARHORSES')

			
			if (iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR') or iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS')):
					if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_HIDDEN_PATHS')):				
						iTech = gc.getInfoTypeForString('TECH_HIDDEN_PATHS')								

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ANCIENT_CHANTS')) :
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CONSTRUCTION')) == False:
						iTech = gc.getInfoTypeForString('TECH_CONSTRUCTION')
						
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):					
				if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
					iTech = gc.getInfoTypeForString('TECH_BRONZE_WORKING')


#Early Techs
#			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')) == False:
#				iTech = gc.getInfoTypeForString('TECH_KNOWLEDGE_OF_THE_ETHER')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SAILING'))== False:
				if pPlayer.countNumCoastalCities() > 0:
					iTech = gc.getInfoTypeForString('TECH_SAILING')						
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ARCHERY')) == False:
				iTech = gc.getInfoTypeForString('TECH_ARCHERY')
			if pPlayer.getNumCities() >= 6 and eTeam.isHasTech(gc.getInfoTypeForString('TECH_CODE_OF_LAWS')) == False :
				if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FINANCIAL')) :
					iTech = gc.getInfoTypeForString('TECH_CODE_OF_LAWS')
					
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY')) == False:
				iTech = gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY')
										
			if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_BARBARIAN')):			
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_WRITING')) == False:
					iTech = gc.getInfoTypeForString('TECH_WRITING')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MYSTICISM')) == False:
				iTech = gc.getInfoTypeForString('TECH_MYSTICISM')
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FESTIVALS')) == False:
				iTech = gc.getInfoTypeForString('TECH_FESTIVALS')			
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CARTOGRAPHY')) == False:
				iTech = gc.getInfoTypeForString('TECH_CARTOGRAPHY')													
			
#Early Religion Beeline

			if not pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC')):
				countreli=0
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS')):
					countreli+=1
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER')):
					countreli+=1
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MESSAGE_FROM_THE_DEEP')):
					countreli+=1
				if countreli==0:

					if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
						iTech = gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER')
					elif pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_NEUTRAL'):
						iTech = gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS')
					elif pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
						iTech = gc.getInfoTypeForString('TECH_MESSAGE_FROM_THE_DEEP')
						
					if iFavRel!=ReligionTypes.NO_RELIGION:
						if iFavRel== gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
							iTech = gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS')
						if iFavRel== gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
							iTech = gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER')
						if iFavRel== gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
							iTech = gc.getInfoTypeForString('TECH_MESSAGE_FROM_THE_DEEP')					

					if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyReligion()!=ReligionTypes.NO_RELIGION:
						newtech = gc.getReligionInfo(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyReligion()).getReligionTech1()
						if eTeam.isHasTech(newtech) == False:
							iTech = newtech
						
					if (iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR') or iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')):
						if pPlayer.canResearch(iTech,False):																				
							iTech = gc.getInfoTypeForString('TECH_WAY_OF_THE_FORESTS')					

					if iCiv == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
						if pPlayer.canResearch(iTech,False):																				
							iTech = gc.getInfoTypeForString('TECH_WAY_OF_THE_EARTHMOTHER')					
						
#Early Happiness for Agnostics						
			else:
				if not eTeam.isHasTech(gc.getInfoTypeForString('TECH_SANITATION')):			
					iTech = gc.getInfoTypeForString('TECH_SANITATION')				
#----------------------------			
#Early Economy
#----------------------------			

		if not bEcon1:
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_EDUCATION')) == False:
				iTech = gc.getInfoTypeForString('TECH_EDUCATION')
				
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_CALENDAR')) == False:
				iTech = gc.getInfoTypeForString('TECH_CALENDAR')
			
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MINING')) == False :
				iTech = gc.getInfoTypeForString('TECH_MINING')
		
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_EXPLORATION')) == False:
				iTech = gc.getInfoTypeForString('TECH_EXPLORATION')
									
#----------------------------			
#Early Military Beeline
#----------------------------

		if not bTier2:
			temp=gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyMilTech()
			if (temp!=TechTypes.NO_TECH):
				iTech = temp
			else:
				iTech = gc.getInfoTypeForString('TECH_BRONZE_WORKING')				
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
					iTech = gc.getInfoTypeForString('TECH_HUNTING')	
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
					iTech = gc.getInfoTypeForString('TECH_HUNTING')	
				if iCiv == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
					iTech = gc.getInfoTypeForString('TECH_CONSTRUCTION')	
#----------------------------
#Calculate Starting resources
#----------------------------
		if (not bEcon1 and not pCity.isNone()):

			sTechs = ['TECH_AGRICULTURE','TECH_CALENDAR','TECH_CRAFTING','TECH_EDUCATION','TECH_HUNTING','TECH_FISHING','TECH_MINING','TECH_ANIMAL_HUSBANDRY']

			lValues = [0]
			for i in range(len(sTechs)):
				lValues=lValues+[0]
			iCount1=-1
			iCount2=-1
			bValid=true
			iX=pCity.getX()
			iY=pCity.getY()

			if iCiv == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
				if pCity.isCoastal(0):
					lValues[sTechs.index('TECH_FISHING')]+=150				

			for iiX in range(iX-2, iX+3, 1):
				iCount1+=1
				for iiY in range(iY-2, iY+3, 1):
					iCount2+=1
					bValid=true
					if iiX==0 and iiY==0:
						bValid=false
					if iiX==0 and iiY==5:
						bValid=false
					if iiX==5 and iiY==0:
						bValid=false
					if iiX==5 and iiY==5:
						bValid=false
					if bValid:
						pLoopPlot = CyMap().plot(iiX,iiY)					
						bBuildinForrest=false
						bBuildinJungle=false
						if (iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR') or iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')):
							bBuildinForrest=true
						if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MINING')):
							bBuildinForrest=true				
						if eTeam.isHasTech(gc.getInfoTypeForString('TECH_BRONZE_WORKING')):
							bBuildinJungle=true											
						if not (pLoopPlot.isNone() or pLoopPlot.isCity()):
		#Fresh Water				
							if pLoopPlot.isFreshWater():
								if not pLoopPlot.isHills():
									iFeature = pLoopPlot.getFeatureType()
									if not (pLoopPlot.getTerrainType() == gc.getInfoTypeForString('TERRAIN_DESERT')):																					
										if (iFeature != gc.getInfoTypeForString('FEATURE_FOREST') or bBuildinForrest):
											if (iFeature != gc.getInfoTypeForString('FEATURE_JUNGLE') or bBuildinJungle):										
												lValues[sTechs.index('TECH_AGRICULTURE')]+=70
										elif not bBuildinForrest:
											lValues[sTechs.index('TECH_MINING')]+=34
									if (iFeature == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')):
										lValues[sTechs.index('TECH_AGRICULTURE')]+=250								
										
			#Fishing
							if pCity.isCoastal(5):
								if pLoopPlot.isWater():
									lValues[sTechs.index('TECH_FISHING')]+=10
										
							eBonus = pLoopPlot.getBonusType(-1)
							if eBonus != BonusTypes.NO_BONUS:
								iFeature = pLoopPlot.getFeatureType()
								if (not iFeature == gc.getInfoTypeForString('FEATURE_FOREST') or bBuildinForrest):
									if (not iFeature == gc.getInfoTypeForString('FEATURE_JUNGLE') or bBuildinJungle):																		
			#Agri						
										if eBonus == gc.getInfoTypeForString('BONUS_WHEAT'):
											lValues[sTechs.index('TECH_AGRICULTURE')]+=350
										if eBonus == gc.getInfoTypeForString('BONUS_CORN') :
											lValues[sTechs.index('TECH_AGRICULTURE')]+=350
										if eBonus == gc.getInfoTypeForString('BONUS_RICE') :
											lValues[sTechs.index('TECH_AGRICULTURE')]+=350
			#Animal Husbandry																																							
										if eBonus == gc.getInfoTypeForString('BONUS_COW') :
											lValues[sTechs.index('TECH_ANIMAL_HUSBANDRY')]+=58								
										if eBonus == gc.getInfoTypeForString('BONUS_SHEEP'):
											lValues[sTechs.index('TECH_ANIMAL_HUSBANDRY')]+=58								
										if eBonus == gc.getInfoTypeForString('BONUS_PIG'):
											lValues[sTechs.index('TECH_ANIMAL_HUSBANDRY')]+=58																
										if eBonus == gc.getInfoTypeForString('BONUS_HORSE'):
											lValues[sTechs.index('TECH_ANIMAL_HUSBANDRY')]+=58																															
			#Crafting													
										if eBonus == gc.getInfoTypeForString('BONUS_WINE') :
											lValues[sTechs.index('TECH_CRAFTING')]+=115
			#Calendar																							
										if eBonus == gc.getInfoTypeForString('BONUS_DYE') :
											lValues[sTechs.index('TECH_CALENDAR')]+=120
										if eBonus == gc.getInfoTypeForString('BONUS_INCENSE') :
											lValues[sTechs.index('TECH_CALENDAR')]+=120
										if eBonus == gc.getInfoTypeForString('BONUS_COTTON') :
											lValues[sTechs.index('TECH_CALENDAR')]+=80
										if eBonus == gc.getInfoTypeForString('BONUS_BANANA') :
											lValues[sTechs.index('TECH_CALENDAR')]+=80
										if eBonus == gc.getInfoTypeForString('BONUS_SILK') :
											lValues[sTechs.index('TECH_CALENDAR')]+=80
										if eBonus == gc.getInfoTypeForString('BONUS_REAGENTS') :
											lValues[sTechs.index('TECH_CALENDAR')]+=80
			#Fishing
										if pCity.isCoastal(5):
											if eBonus == gc.getInfoTypeForString('BONUS_CLAM'):
												lValues[sTechs.index('TECH_FISHING')]+=40
											if eBonus == gc.getInfoTypeForString('BONUS_CRAB') :
												lValues[sTechs.index('TECH_FISHING')]+=40
											if eBonus == gc.getInfoTypeForString('BONUS_FISH') :
												lValues[sTechs.index('TECH_FISHING')]+=40
											if iCiv == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
												if eBonus == gc.getInfoTypeForString('BONUS_PEARL') :
													lValues[sTechs.index('TECH_FISHING')]+=200																
			#Hunting					
										if pPlayer.getResearchTurnsLeft(gc.getInfoTypeForString('TECH_HUNTING'),true)<20:			
											if eBonus == gc.getInfoTypeForString('BONUS_DEER'):
												lValues[sTechs.index('TECH_HUNTING')]+=80																
											if eBonus == gc.getInfoTypeForString('BONUS_FUR'):
												lValues[sTechs.index('TECH_HUNTING')]+=110																
											if eBonus == gc.getInfoTypeForString('BONUS_IVORY'):
												lValues[sTechs.index('TECH_HUNTING')]+=110
			#Mining															
										if eBonus == gc.getInfoTypeForString('BONUS_GOLD'):
											lValues[sTechs.index('TECH_MINING')]+=200
										if eBonus == gc.getInfoTypeForString('BONUS_GEMS') :
											lValues[sTechs.index('TECH_MINING')]+=200
										
								else: 
									lValues[sTechs.index('TECH_MINING')]+=50
							
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
				lValues[sTechs.index('TECH_ANIMAL_HUSBANDRY')]+=50																
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
				lValues[sTechs.index('TECH_FISHING')]*=2

			iBestTech=-1
			iBestTechValue=99
			for i in range(len(sTechs)):
				if lValues[i]>iBestTechValue:
					if (eTeam.isHasTech(gc.getInfoTypeForString(sTechs[i])) == False): 
						iBestTechValue=lValues[i]
						iBestTech=i


			bNeedmoreResearch = true						
			if iBestTech!=-1:
				iTech=gc.getInfoTypeForString(sTechs[iBestTech])
				bNeedmoreResearch = false
#				CyInterface().addMessage(0,true,25,"This is Player %s: best Research is (%i)" %(pPlayer.getName(),iBestTech),'',0,'',ColorTypes(11), 0, 0, True,True)							

			elif not eTeam.isHasTech(gc.getInfoTypeForString('TECH_FESTIVALS')):
					iTech = gc.getInfoTypeForString('TECH_FESTIVALS')	

			elif not bTier2:
				iturns=15
				if CyGame().getGameTurn()>100:
					iturns+=10
				if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyMilTech()!=TechTypes.NO_TECH:
					if pPlayer.getResearchTurnsLeft(gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyMilTech(),false)<iturns:
						iTech = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyMilTech()
						bNeedmoreResearch=false
				else:
					if eTeam.isHasTech(gc.getInfoTypeForString('TECH_MINING')):
						if pPlayer.getResearchTurnsLeft(gc.getInfoTypeForString('TECH_BRONZE_WORKING'),false)<iturns:
							iTech = gc.getInfoTypeForString('TECH_BRONZE_WORKING')
							bNeedmoreResearch=false
					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_ANIMAL_HUSBANDRY')):
						if pPlayer.getResearchTurnsLeft(gc.getInfoTypeForString('TECH_HORSEBACK_RIDING'),true)<iturns:
							iTech = gc.getInfoTypeForString('TECH_HORSEBACK_RIDING')							
							bNeedmoreResearch=false						
					elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_EXPLORATION')):
						if pPlayer.getResearchTurnsLeft(gc.getInfoTypeForString('TECH_HUNTING'),true)<iturns:
							iTech = gc.getInfoTypeForString('TECH_HUNTING')
							bNeedmoreResearch=false

		
			
			if bNeedmoreResearch:
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_EXPLORATION')) == False:
					iTech = gc.getInfoTypeForString('TECH_EXPLORATION')								
				elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_FESTIVALS')) == False:
					iTech = gc.getInfoTypeForString('TECH_FESTIVALS')								
				elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_MYSTICISM')) == False:
					iTech = gc.getInfoTypeForString('TECH_MYSTICISM')					
				elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_EDUCATION')) == False:
					iTech = gc.getInfoTypeForString('TECH_EDUCATION')			
				elif eTeam.isHasTech(gc.getInfoTypeForString('TECH_CARTOGRAPHY')) == False and pPlayer.getNumCities()>4:
					iTech = gc.getInfoTypeForString('TECH_CARTOGRAPHY')													
				else:
					if not bTier2:
						if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyMilTech()!=TechTypes.NO_TECH:
							iTech = gc.getLeaderHeadInfo(pPlayer.getLeaderType()).getFavoriteEarlyMilTech()
						else:
							iTech = gc.getInfoTypeForString('TECH_BRONZE_WORKING')

		if pPlayer.getNumCities()==0:
			return gc.getInfoTypeForString('TECH_AGRICULTURE')
		
		if iTech != -1:			
			if eTeam.isHasTech(iTech) == False:
				return iTech

				
		return TechTypes.NO_TECH

	def AI_chooseProduction(self,argsList):
		pCity = argsList[0]
		ePlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(ePlayer)
		player = PyPlayer(ePlayer)
		civtype = pPlayer.getCivilizationType()
		infoCiv = gc.getCivilizationInfo(civtype)
		eTeam = gc.getTeam(pPlayer.getTeam())
		pPlot = pCity.plot()

#Barbarian Cities have their own Function
		if pCity.isBarbarian():
			if (cf.BarbCityProduction(pCity)==0):
				return False
			else:
				return True

#Automated Cities use another Function
		if pPlayer.isHuman():
			return False

#Choose Nothing in Disorder (can lead to weird results)
		if pCity.isDisorder():
			return False
			
#Var initialization
		#Used for City Specialization
		iPatrolSpec=0
		iDefenseSpec=0

		#Used to decide if the Best Item is good enough
		diffmod = 0.8
		iBuildingthres=0
		iBuildingthres+=1000
		iBuildingthres+=-13*pCity.getCurrentProductionDifference(False,False)
		iBuildingthres=(iBuildingthres)*diffmod
		iBuildingthres=-pPlayer.countGroupFlagUnits(7)*50

#make sure no item is listed twice!
#Use BuildingClass if Possible
		sProd = ['PROJECT_BLOOD_OF_THE_PHOENIX','PROJECT_GENESIS','PROJECT_RITES_OF_OGHMA','PROJECT_NATURES_REVOLT']
		iProdType=[3,3,3,3]		
		sProd = sProd +['PROJECT_ELEGY_OF_THE_SHEAIM','PROJECT_HALLOWING_OF_THE_ELOHIM','PROJECT_BIRTHRIGHT_REGAINED','PROJECT_PURGE_THE_UNFAITHFUL']
		iProdType=iProdType+[3,3,3,3]		
		sProd = sProd +['PROJECT_SAMHAIN','PROJECT_THE_WHITE_HAND','PROJECT_THE_DEEPENING','PROJECT_STIR_FROM_SLUMBER']
		iProdType=iProdType+[3,3,3,3]		
		sProd = sProd +['PROJECT_THE_DRAW','PROJECT_ASCENSION','PROJECT_PACT_OF_THE_NILHORN']
		iProdType=iProdType+[3,3,3]		
				
		sProd = sProd +['UNITCLASS_SETTLER','UNITCLASS_WORKER','UNITCLASS_WARRIOR','UNITCLASS_WORKBOAT','UNITCLASS_SCOUT']
		iProdType=iProdType+[2,2,2,2,2]		
		sProd = sProd + ['UNITCLASS_ADEPT','UNITCLASS_AXEMAN','UNITCLASS_HUNTER','UNITCLASS_ARCHER','UNITCLASS_HORSEMAN','UNITCLASS_HORSE_ARCHER']
		iProdType=iProdType+[2,2,2,2,2,2]
		sProd = sProd + ['UNITCLASS_FREAK','UNITCLASS_CATAPULT','UNITCLASS_CANNON','UNITCLASS_MONK','UNITCLASS_GRIGORI_MEDIC']
		iProdType=iProdType+[2,2,2,2,2]
		sProd = sProd + ['UNITCLASS_PRIEST_OF_THE_VEIL','UNITCLASS_PRIEST_OF_THE_ORDER','UNITCLASS_PRIEST_OF_KILMORPH','UNITCLASS_PRIEST_OF_LEAVES','UNITCLASS_PRIEST_OF_THE_EMPYREAN','UNITCLASS_PRIEST_OF_THE_OVERLORDS']
		iProdType=iProdType+[2,2,2,2,2,2]					
		sProd = sProd + ['UNITCLASS_DISCIPLE_THE_ASHEN_VEIL','UNITCLASS_DISCIPLE_THE_ORDER','UNITCLASS_DISCIPLE_RUNES_OF_KILMORPH','UNITCLASS_DISCIPLE_FELLOWSHIP_OF_LEAVES','UNITCLASS_DISCIPLE_EMPYREAN','UNITCLASS_DISCIPLE_OCTOPUS_OVERLORDS']
		iProdType=iProdType+[2,2,2,2,2,2]
		sProd = sProd + ['UNITCLASS_CHAMPION','UNITCLASS_CHARIOT','UNITCLASS_RANGER','UNITCLASS_LONGBOWMAN','UNITCLASS_ASSASSIN']
		iProdType=iProdType+[2,2,2,2,2]
		sProd = sProd + ['UNITCLASS_GOVANNON','UNITCLASS_LOKI','UNITCLASS_DONAL','UNITCLASS_RANTINE','UNITCLASS_LOSHA']
		iProdType=iProdType+[2,2,2,2,2]
		sProd = sProd + ['UNITCLASS_GALLEY','UNITCLASS_CARAVEL','UNITCLASS_EXPLORER','UNITCLASS_QUEEN_OF_THE_LINE']
		iProdType=iProdType+[2,2,2,2]
		sProd = sProd + ['UNITCLASS_TRIREME','UNITCLASS_FRIGATE','UNITCLASS_MAN_O_WAR']
		iProdType=iProdType+[2,2,2]	

		sProd = sProd + ['BUILDINGCLASS_ALCHEMY_LAB','BUILDINGCLASS_AQUEDUCT','BUILDINGCLASS_TRAINING_YARD','BUILDINGCLASS_BASILICA','BUILDINGCLASS_BREWERY']
		iProdType=iProdType+[1,1,1,1,1]
		sProd = sProd + ['BUILDINGCLASS_CARNIVAL','BUILDINGCLASS_COURTHOUSE','BUILDINGCLASS_DUNGEON','BUILDINGCLASS_ELDER_COUNCIL','BUILDINGCLASS_ARCHERY_RANGE','BUILDINGCLASS_FORGE','BUILDINGCLASS_GAMBLING_HOUSE','BUILDINGCLASS_GRANARY']
		iProdType=iProdType+[1,1,1,1,1,1,1,1]
		sProd = sProd + ['BUILDINGCLASS_GROVE','BUILDINGCLASS_HARBOR','BUILDINGCLASS_HERBALIST','BUILDINGCLASS_HUNTING_LODGE','BUILDINGCLASS_INFIRMARY','BUILDINGCLASS_INN','BUILDINGCLASS_LIBRARY','BUILDINGCLASS_LIGHTHOUSE','BUILDINGCLASS_MACHINISTS_SHOP']
		iProdType=iProdType+[1,1,1,1,1,1,1,1,1]
		sProd = sProd + ['BUILDINGCLASS_MAGE_GUILD','BUILDINGCLASS_MARKET','BUILDINGCLASS_MONEYCHANGER','BUILDINGCLASS_MONUMENT','BUILDINGCLASS_PAGAN_TEMPLE','BUILDINGCLASS_PALISADE']
		iProdType=iProdType+[1,1,1,1,1,1]
		sProd = sProd + ['BUILDINGCLASS_PUBLIC_BATHS','BUILDINGCLASS_SIEGE_WORKSHOP','BUILDINGCLASS_SMOKEHOUSE','BUILDINGCLASS_STABLE','BUILDINGCLASS_TAX_OFFICE','BUILDINGCLASS_TAVERN']
		iProdType=iProdType+[1,1,1,1,1,1]				
		sProd = sProd + ['BUILDINGCLASS_TEMPLE_OF_KILMORPH','BUILDINGCLASS_TEMPLE_OF_LEAVES','BUILDINGCLASS_TEMPLE_OF_THE_EMPYREAN','BUILDINGCLASS_TEMPLE_OF_THE_OVERLORDS','BUILDINGCLASS_TEMPLE_OF_THE_VEIL','BUILDINGCLASS_TEMPLE_OF_THE_ORDER']
		iProdType=iProdType+[1,1,1,1,1,1]				
		sProd = sProd + ['BUILDINGCLASS_THEATRE','BUILDINGCLASS_WALLS']
		iProdType=iProdType+[1,1]

		sProd = sProd + ['BUILDINGCLASS_TOWER_OF_ALTERATION','BUILDINGCLASS_TOWER_OF_DIVINATION','BUILDINGCLASS_TOWER_OF_NECROMANCY','BUILDINGCLASS_TOWER_OF_THE_ELEMENTS','BUILDINGCLASS_TOWER_OF_MASTERY','BUILDINGCLASS_ALTAR_OF_THE_LUONNOTAR_FINAL']
		iProdType=iProdType+[1,1,1,1,1,1]

		sProd = sProd + ['BUILDINGCLASS_GUILD_OF_THE_NINE','BUILDINGCLASS_HERON_THRONE','BUILDINGCLASS_CITY_OF_A_THOUSAND_SLUMS','BUILDINGCLASS_THEATRE_OF_DREAMS','BUILDINGCLASS_PILLAR_OF_CHAINS']
		iProdType=iProdType+[1,1,1,1,1]		
		sProd = sProd + ['BUILDINGCLASS_GUILD_OF_HAMMERS','BUILDINGCLASS_GRAND_MENAGERIE','BUILDINGCLASS_MERCURIAN_GATE','BUILDINGCLASS_CELESTIAL_COMPASS','BUILDINGCLASS_RIDE_OF_THE_NINE_KINGS']
		iProdType=iProdType+[1,1,1,1,1]		
		sProd = sProd + ['BUILDINGCLASS_MOKKAS_CAULDRON','BUILDINGCLASS_SHRINE_OF_SIRONA','BUILDINGCLASS_EYES_AND_EARS_NETWORK','BUILDINGCLASS_SHRINE_OF_THE_CHAMPION','BUILDINGCLASS_AQUAE_SUCELLUS']
		iProdType=iProdType+[1,1,1,1,1]		
		sProd = sProd + ['BUILDINGCLASS_HALL_OF_KINGS','BUILDINGCLASS_GREAT_LIBRARY','BUILDINGCLASS_GREAT_LIGHTHOUSE','BUILDINGCLASS_PROPHECY_OF_RAGNAROK','BUILDINGCLASS_TEMPLE_OF_TEMPORENCE']
		iProdType=iProdType+[1,1,1,1,1]		
		sProd = sProd + ['BUILDINGCLASS_HEROIC_EPIC','BUILDINGCLASS_NATIONAL_EPIC','BUILDINGCLASS_TOWER_OF_COMPLACENCY','BUILDINGCLASS_TOWER_OF_EYES','BUILDINGCLASS_SYLIVENS_PERFECT_LYRE']
		iProdType=iProdType+[1,1,1,1,1]		
		sProd = sProd + ['BUILDINGCLASS_CROWN_OF_AKHARIEN','BUILDINGCLASS_FORBIDDEN_PALACE','BUILDINGCLASS_CATACOMB_LIBRALUS','BUILDINGCLASS_FORM_OF_THE_TITAN','BUILDINGCLASS_MINES_OF_GALDUR']
		iProdType=iProdType+[1,1,1,1,1]		
		sProd = sProd + ['BUILDINGCLASS_BAZAAR_OF_MAMMON']
		iProdType=iProdType+[1]

		sProd = sProd + ['BUILDING_ADULARIA_CHAMBER','BUILDING_ADVENTURERS_GUILD','BUILDING_BLASTING_WORKSHOP','BUILDING_BREEDING_PIT','BUILDING_CAVE_OF_ANCESTORS','BUILDING_CHANCEL_OF_GUARDIANS','BUILDING_CITADEL_OF_LIGHT','BUILDING_COMMAND_POST']
		iProdType=iProdType+[0,0,0,0,0,0,0,0]
		sProd = sProd + ['BUILDING_HALL_OF_MIRRORS']
		iProdType=iProdType+[0]
		sProd = sProd + ['BUILDING_JEWELER','BUILDING_PALLENS_ENGINE','BUILDING_PLANAR_GATE','BUILDING_RELIQUARY']
		iProdType=iProdType+[0,0,0,0]
		sProd = sProd + ['BUILDING_SMUGGLERS_PORT','BUILDING_TAILOR','BUILDING_WARRENS','BUILDING_MONUMENT']
		iProdType=iProdType+[0,0,0,0]

		iValue=[0]
		for i in range (len(sProd)):
			iValue+=[0]

#City needs more Protection? (values 19001-20000)
		if (pCity.AI_neededPermDefense(0)>0):
						
			iValue[sProd.index('UNITCLASS_AXEMAN')]=19500
			iValue[sProd.index('UNITCLASS_ARCHER')]=20000
			iValue[sProd.index('UNITCLASS_HUNTER')]=19500
			iValue[sProd.index('UNITCLASS_WARRIOR')]=19002

		if (pCity.AI_neededPermDefense(1)>0):
		
			iValue[sProd.index('UNITCLASS_AXEMAN')]=20000
			iValue[sProd.index('UNITCLASS_ARCHER')]=19500
			iValue[sProd.index('UNITCLASS_HUNTER')]=20000
			iValue[sProd.index('UNITCLASS_WARRIOR')]=19003
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):			
				iValue[sProd.index('UNITCLASS_AXEMAN')]=-20000
		
		if (pCity.AI_neededPermDefense(2)>0):
			iValue[sProd.index('UNITCLASS_ADEPT')]=19002		
		
		if (pCity.AI_neededPermDefense(3)>0):		
			iValue[sProd.index('UNITCLASS_PRIEST_OF_LEAVES')]=19500				
			iValue[sProd.index('UNITCLASS_PRIEST_OF_KILMORPH')]=19500				
			iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_EMPYREAN')]=19500				
			iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_OVERLORDS')]=19500				
			iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_VEIL')]=19500				
			iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_ORDER')]=19500				

#WAR: Cities close by need more Protection? (values 18001-19000)						
		iTeam = gc.getTeam(pPlayer.getTeam())
		if iTeam.getAtWarCount(True)>0:

			if (pPlot.AI_neededPermDefenseReserve(0)>0):

				iValue[sProd.index('UNITCLASS_AXEMAN')]=18500
				iValue[sProd.index('UNITCLASS_ARCHER')]=19000
				iValue[sProd.index('UNITCLASS_HUNTER')]=18500
				iValue[sProd.index('UNITCLASS_WARRIOR')]=18001
				
			if (pPlot.AI_neededPermDefenseReserve(1)>0):
			
				iValue[sProd.index('UNITCLASS_AXEMAN')]=19000
				iValue[sProd.index('UNITCLASS_ARCHER')]=18500
				iValue[sProd.index('UNITCLASS_HUNTER')]=19000
				iValue[sProd.index('UNITCLASS_WARRIOR')]=18001
			
			if (pPlot.AI_neededPermDefenseReserve(2)>0):
				iValue[sProd.index('UNITCLASS_ADEPT')]=18001

			if (pPlot.AI_neededPermDefenseReserve(3)>0):
				iValue[sProd.index('UNITCLASS_PRIEST_OF_LEAVES')]=18500
				iValue[sProd.index('UNITCLASS_PRIEST_OF_KILMORPH')]=18500
				iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_EMPYREAN')]=18500
				iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_OVERLORDS')]=18500
				iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_VEIL')]=18500
				iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_ORDER')]=18500
				iValue[sProd.index('UNITCLASS_GRIGORI_MEDIC')]=18500
				

#WAR: Citypatrol need more Units? (values 17001-18000)			
		if iTeam.getAtWarCount(True)>0:	
							
			if pCity.AI_neededPatrol(0)>0:
				iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]=17002
				iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=17003
				iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=17004

				iValue[sProd.index('UNITCLASS_AXEMAN')]=17500
				iValue[sProd.index('UNITCLASS_ARCHER')]=17500
				iValue[sProd.index('UNITCLASS_HUNTER')]=18000
				iValue[sProd.index('UNITCLASS_WARRIOR')]=17001
				
			if (pCity.AI_neededPatrol(1)>0):		
				iValue[sProd.index('UNITCLASS_ADEPT')]=17001
				
#This is a City for Patrol Units?
		if pCity.AI_neededCityPatrolProduction(1)>0:
			iPatrolSpec=13000
			if pCity.isCapital():		#make sure patrol is build before first settler
				iPatrolSpec+=4000
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]=iPatrolSpec+2
			iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iPatrolSpec+3
			iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iPatrolSpec+4

			if pCity.AI_neededPatrol(0)>0:
				iValue[sProd.index('UNITCLASS_AXEMAN')]=iPatrolSpec+500
				iValue[sProd.index('UNITCLASS_ARCHER')]=iPatrolSpec+500
				iValue[sProd.index('UNITCLASS_HUNTER')]=iPatrolSpec+500
				iValue[sProd.index('UNITCLASS_WARRIOR')]=iPatrolSpec+1

			if (pCity.AI_neededPatrol(1)>0):
				iValue[sProd.index('UNITCLASS_ADEPT')]=iPatrolSpec+1

#Defense specialization:
		elif pCity.AI_neededCityDefenseProduction(2)>0:
			iDefenseSpec=12000
			iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=iDefenseSpec
			iValue[sProd.index('UNITCLASS_LONGBOWMAN')]+=iDefenseSpec

		elif pCity.AI_neededCityDefenseProduction(1)>0:
			iDefenseSpec=12000
			iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=iDefenseSpec
			iValue[sProd.index('UNITCLASS_ARCHER')]+=iDefenseSpec

		iSpecialization=iPatrolSpec	#Count how much Value the Specialization of a City has
		if iSpecialization<iDefenseSpec:
			iSpecialization=iDefenseSpec
			
#Civ Needs more workboats?
		if not (pCity.waterArea().isNone()):
			if pPlayer.AI_totalWaterAreaUnitAIs(pCity.waterArea(),gc.getInfoTypeForString('UNITAI_WORKER_SEA'))==0:
				if pCity.AI_neededSeaWorkers()>0:
					iValue[sProd.index('UNITCLASS_WORKBOAT')]=19002				
		
# Civ needs more workers?
		if 2 * pPlayer.getNumCities() > pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_WORKER')):
			if pCity.isCapital() or ((pCity.getCurrentProductionDifference(True,False)>7 and pCity.getPopulation() > 3)):
				if (pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_WORKER'))<(pPlayer.getNumCities()+pPlayer.getNumCities()-1-pPlayer.getNumCities()/3)):
					iValue[sProd.index('UNITCLASS_WORKER')]=16001
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_WORKER'))==0:
					iValue[sProd.index('UNITCLASS_WORKER')]=19001		
				else:
					iValue[sProd.index('UNITCLASS_WORKER')]+=300+(3/2*pPlayer.getNumCities()/(1+pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_WORKER'))))*1000

		
					
# Civ needs more Settlers?
		if	(not pPlayer.isConquestMode()) or pPlayer.countGroupFlagUnits(10)>20:
			if pPlayer.getNumCities() < pPlayer.getMaxCities() or pPlayer.getMaxCities()<=0:
				bvalid=false
				if (pCity.getCurrentProductionDifference(True,False)>10 and pCity.getPopulation() > 4):
					if not pCity.isCapital():
						bvalid=true
				if pCity.isCapital():
					if pCity.happyLevel()<=pCity.unhappyLevel(0) or (pCity.foodDifference(false)<2):
						bvalid=true										
				if bvalid:
					iSettlerBadlyNeeded=1				
					if pPlayer.getNumCities()>3:
						iSettlerBadlyNeeded=2+pPlayer.getNumCities()/10
					if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_SETTLER'))<iSettlerBadlyNeeded:
						iValue[sProd.index('UNITCLASS_SETTLER')]=17000

#Civ Needs more Barbsmashers?
		if not pPlayer.isConquestMode():
			if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_SETTLER'))>0:		
				if pPlayer.countGroupFlagUnits(7)<10:	# 7 is GROUPFLAG_DEFENSE_NEW
					iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=2502
					iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=2503
					iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]+=2504

					iValue[sProd.index('UNITCLASS_AXEMAN')]+=2500
					iValue[sProd.index('UNITCLASS_ARCHER')]+=2500
					iValue[sProd.index('UNITCLASS_HUNTER')]+=2500
					iValue[sProd.index('UNITCLASS_WARRIOR')]+=2501
						
#Civ can build a Religion Hero?
		if pPlayer.getFavoriteReligion()!=ReligionTypes.NO_RELIGION:
			if (gc.getReligionInfo(pPlayer.getFavoriteReligion()).getReligionHero1()!=UnitClassTypes.NO_UNITCLASS):
				if pPlayer.getUnitClassCountPlusMaking(gc.getReligionInfo(pPlayer.getFavoriteReligion()).getReligionHero1())==0:
					tUnit = gc.getUnitClassInfo(gc.getReligionInfo(pPlayer.getFavoriteReligion()).getReligionHero1()).getDefaultUnitIndex()
					if pCity.canTrain(tUnit,True,False):
						if pCity.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION)<3:
							pCity.pushOrder(OrderTypes.ORDER_TRAIN,tUnit,-1, False, False, False, False)			
							return 1			
			if (gc.getReligionInfo(pPlayer.getFavoriteReligion()).getReligionHero2()!=UnitClassTypes.NO_UNITCLASS):						
				if pPlayer.getUnitClassCountPlusMaking(gc.getReligionInfo(pPlayer.getFavoriteReligion()).getReligionHero2())==0:			
					tUnit = gc.getUnitClassInfo(gc.getReligionInfo(pPlayer.getFavoriteReligion()).getReligionHero2()).getDefaultUnitIndex()					
					if pCity.canTrain(tUnit,True,False):
						if pCity.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION)<3:
							pCity.pushOrder(OrderTypes.ORDER_TRAIN,tUnit,-1, False, False, False, False)			
							return 1			

#Civ can build its Hero?
		if pCity.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION)<3:		
			iLoki= gc.getInfoTypeForString('UNIT_LOKI')		
			iHero= gc.getCivilizationInfo(pPlayer.getCivilizationType()).getHero()
			if (iHero!=UnitTypes.NO_UNIT and iHero!=iLoki):				
				if pCity.canTrain(iHero,True,False):
					pCity.pushOrder(OrderTypes.ORDER_TRAIN,iHero,-1, False, False, False, False)			
					return 1			

		iCountNavalTransporters=pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_GALLEY'))
		iCountNavalTransporters+=pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_CARAVEL'))
		iCountNavalTransporters+=pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_QUEEN_OF_THE_LINE'))		
		iCountNavalPatrols=pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_TRIREME'))
		iCountNavalPatrols+=pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_FRIGATE'))
		iCountNavalPatrols+=pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_MAN_O_WAR'))
		
		if pPlayer.getUnitClassCount(gc.getInfoTypeForString('UNITCLASS_SETTLER'))>0:
#Need to add check that settlerships are only build for naval settle mission		
			if iCountNavalTransporters<3:
				iValue[sProd.index('UNITCLASS_GALLEY')]+=1500
				iValue[sProd.index('UNITCLASS_CARAVEL')]+=1500
				iValue[sProd.index('UNITCLASS_QUEEN_OF_THE_LINE')]+=1500				

		if iCountNavalPatrols<pPlayer.getNumCities():
			iValue[sProd.index('UNITCLASS_TRIREME')]+=1500			
			iValue[sProd.index('UNITCLASS_FRIGATE')]+=1500			
			iValue[sProd.index('UNITCLASS_MAN_O_WAR')]+=1500			
			
# Civ needs more terraformers?

		countmages=0
		countPriests=0
		player = PyPlayer(pCity.getOwner())		
		for pUnit in player.getUnitList():    #rewrite this into the dll
			if pUnit.getUnitAIType() == gc.getInfoTypeForString('UNITAI_TERRAFORMER'):
				countmages = countmages+1
			if pUnit.getUnitAIType() == gc.getInfoTypeForString('UNITAI_MANA_UPGRADE'):	
				countmages = countmages+1
			if pUnit.getUnitType() == 	gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'):
				if pUnit.getUnitAIType() == gc.getInfoTypeForString('UNITAI_TERRAFORMER'):
					countPriests=countPriests+1
					
		if countmages<2: #need to write a Calculation for terraformer per area
			iValue[sProd.index('UNITCLASS_ADEPT')]+=1000			
		if countPriests<2: 
			iValue[sProd.index('UNITCLASS_PRIEST_OF_LEAVES')]+=1000
			
# City has enough Culture?
		if pCity.getCulture(pCity.getOwner())==0:
			iValue[sProd.index('BUILDING_MONUMENT')]=1100+iSpecialization

# Every City should have atleast a training yard, archery range or hunting lodge			
		iBuilding1 = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_TRAINING_YARD'))
		iBuilding2 = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))
		iBuilding3 = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))		
		iCount=0
		if (iBuilding1!=-1):
			if pCity.getNumBuilding(iBuilding1)==1:
				iCount+=1
		if (iBuilding2!=-1):
			if pCity.getNumBuilding(iBuilding2)==1:
				iCount+=1
		if (iBuilding3!=-1):
			if pCity.getNumBuilding(iBuilding3)==1:
				iCount+=1
		#some Civs prefere a different Building
		if civtype == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
			if iCount==0:
				iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]+=1200
				iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=1200
				iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]+=1200

		else:
			if iCount==0:
				iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=1200
				iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=1200
				iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]+=1200

		if (iCount>0):
# Empire needs another Military Building?
			iBuilding4 = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))
			iBuilding5 = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))
			iBuilding6 = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))
			iCount=0
			if (iBuilding4!=-1):
				if pCity.getNumBuilding(iBuilding4)==1:
					iCount+=1
			if (iBuilding5!=-1):
				if pCity.getNumBuilding(iBuilding5)==1:
					iCount+=1
			if (iBuilding6!=-1):
				if pCity.getNumBuilding(iBuilding6)==1:
					iCount+=1
			if iCount==0:
				iValue[sProd.index('BUILDINGCLASS_STABLE')]+=0
			iValue[sProd.index('BUILDINGCLASS_STABLE')]+=200*pPlayer.getNumCities()/(1+pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE')))
			if iCount==0:
				iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]+=0
			iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]+=200*pPlayer.getNumCities()/(1+pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP')))
			if iCount==0:
				iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]+=0
			iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]+=200*pPlayer.getNumCities()/(1+pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD')))
#Temples and disciples

		if not (pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC'))):
			religioncount=0			
			ireligion=pPlayer.getStateReligion()
			bonus=0+iSpecialization
			if ireligion==pPlayer.getFavoriteReligion():
				bonus+=3000
			if ireligion==gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_LEAVES')]+=400+20*pCity.getCurrentProductionDifference(False,False)+bonus
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_DISCIPLE_FELLOWSHIP_OF_LEAVES'))==0:
					iValue[sProd.index('UNITCLASS_DISCIPLE_FELLOWSHIP_OF_LEAVES')]+=3000

			if ireligion==gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):
				iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_KILMORPH')]+=400+20*pCity.getCurrentProductionDifference(False,False)+bonus
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_DISCIPLE_RUNES_OF_KILMORPH'))==0:
					iValue[sProd.index('UNITCLASS_DISCIPLE_RUNES_OF_KILMORPH')]+=3000

			if ireligion==gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_EMPYREAN')]+=400+20*pCity.getCurrentProductionDifference(False,False)+bonus
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_DISCIPLE_EMPYREAN'))==0:
					iValue[sProd.index('UNITCLASS_DISCIPLE_EMPYREAN')]+=3000

			if ireligion==gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):
				iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_OVERLORDS')]+=400+20*pCity.getCurrentProductionDifference(False,False)+bonus
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_DISCIPLE_OCTOPUS_OVERLORDS'))==0:
					iValue[sProd.index('UNITCLASS_DISCIPLE_OCTOPUS_OVERLORDS')]+=3000

			if ireligion==gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):
				iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_VEIL')]+=400+20*pCity.getCurrentProductionDifference(False,False)+bonus
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_DISCIPLE_THE_ASHEN_VEIL'))==0:
					iValue[sProd.index('UNITCLASS_DISCIPLE_THE_ASHEN_VEIL')]+=3000
				iValue[sProd.index('BUILDINGCLASS_PROPHECY_OF_RAGNAROK')]=2000								

			if ireligion==gc.getInfoTypeForString('RELIGION_THE_ORDER'):
				iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_ORDER')]+=400+20*pCity.getCurrentProductionDifference(False,False)+bonus
				if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_DISCIPLE_THE_ORDER'))==0:
					iValue[sProd.index('UNITCLASS_DISCIPLE_THE_ORDER')]+=3000

			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isReligionVictory():
				if CyGame().getHolyCity(gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES')).getOwner()==ePlayer:
					if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_DISCIPLE_FELLOWSHIP_OF_LEAVES'))<pPlayer.getNumCities()*3:
						iValue[sProd.index('UNITCLASS_DISCIPLE_FELLOWSHIP_OF_LEAVES')]+=3000

# City can build civ specific buildings?	

#init for Conquestmode		
		iDif=8+2*int(CyGame().getHandicapType()) #used for Conquest Modus
		iMinCitySize=7
		iReli=-1
		sReli=''
		iReliMod=0
		totalpriests=0
		if not (pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC'))):
			ireligion=pPlayer.getStateReligion()
			if ireligion==gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'):
				iReli=gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_LEAVES')
				sReli='UNITCLASS_PRIEST_OF_LEAVES'
				iReliMod+=2
			if ireligion==gc.getInfoTypeForString('RELIGION_RUNES_OF_KILMORPH'):		
				iReli=gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_KILMORPH')
				sReli='UNITCLASS_PRIEST_OF_KILMORPH'
				iReliMod+=0
			if ireligion==gc.getInfoTypeForString('RELIGION_THE_EMPYREAN'):
				iReli=gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_EMPYREAN')
				sReli='UNITCLASS_PRIEST_OF_THE_EMPYREAN'
				iReliMod+=0
			if ireligion==gc.getInfoTypeForString('RELIGION_OCTOPUS_OVERLORDS'):		
				iReli=gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_OVERLORDS')
				sReli='UNITCLASS_PRIEST_OF_THE_OVERLORDS'
				iReliMod+=1
			if ireligion==gc.getInfoTypeForString('RELIGION_THE_ASHEN_VEIL'):			
				iReli=gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_VEIL')
				sReli='UNITCLASS_PRIEST_OF_THE_VEIL'
				iReliMod+=2				
			if ireligion==gc.getInfoTypeForString('RELIGION_THE_ORDER'):			
				iReli=gc.getInfoTypeForString('UNITCLASS_PRIEST_OF_THE_ORDER')
				sReli='UNITCLASS_PRIEST_OF_THE_ORDER'
				iReliMod+=0				

#Amurites
		if civtype == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
			if pCity.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION)<3:				
				iValue[sProd.index('UNITCLASS_GOVANNON')]+=19000
				iValue[sProd.index('BUILDINGCLASS_CATACOMB_LIBRALUS')]+=3000								
			if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_MAGE_GUILD'))==1:						
				iValue[sProd.index('BUILDING_CAVE_OF_ANCESTORS')]+=630
			if	pPlayer.isConquestMode():
				iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=-10000			
				if ((pCity.getPopulation()>iMinCitySize+3) or (pCity.foodDifference(False)<1)):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:		# 10 is GROUPFLAG_CONQUEST
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
						
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalmounted+totalpriests					
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+7*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_LONGBOWMAN')]+=1200+15*(totalunits-totalarchers)							
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+10*(totalunits-totalmelee)							
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)												
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+10*(totalunits-totalmounted)																		
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)*iReliMod
						
						iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=12000												
						iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=12000
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TRAINING_YARD'))*5:
							iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]=iValue[sProd.index('UNITCLASS_AXEMAN')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10

#Balseraph
		if civtype == gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=250
			iValue[sProd.index('BUILDING_HALL_OF_MIRRORS')]==300
			if pCity.isCapital():
				if eTeam.isHasTech(gc.getInfoTypeForString('TECH_FESTIVALS')):
					iValue[sProd.index('UNITCLASS_LOKI')]+=12000			
			if pPlayer.isConquestMode():
				if ((pCity.getPopulation()>iMinCitySize) or (pCity.foodDifference(False)<1)):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())

						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+3*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+14*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+11*(totalunits-totalsiege)					
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+10*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]=12000
						iValue[sProd.index('UNITCLASS_FREAK')]=iValue[sProd.index('UNITCLASS_AXEMAN')]+3
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*3:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10											

#Bannor
		if civtype == gc.getInfoTypeForString('CIVILIZATION_BANNOR'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=250
			if pCity.isCapital():
				iValue[sProd.index('UNITCLASS_DONAL')]+=12000	
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>iMinCitySize or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+10*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)												
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+11*(totalunits-totalsiege)																								
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)																								
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]=12000											
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*3:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				
							
#Calabim
		if civtype == gc.getInfoTypeForString('CIVILIZATION_CALABIM'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=250
			iValue[sProd.index('BUILDING_BREEDING_PIT')]+=750
			iValue[sProd.index('BUILDINGCLASS_COURTHOUSE')]+=800			
			if pCity.isCapital():
				iValue[sProd.index('UNITCLASS_LOSHA')]+=12000				
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>iMinCitySize or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+12*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+9*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)

						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)												
#						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]=12000											
						iValue[sProd.index('BUILDINGCLASS_COURTHOUSE')]+=12000									
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				
							
#Clan of Embers
		if civtype == gc.getInfoTypeForString('CIVILIZATION_CLAN_OF_EMBERS'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=250
			iValue[sProd.index('BUILDING_WARRENS')]+=70*pCity.getCurrentProductionDifference(False,False)+iSpecialization						
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize-3) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+15*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+8*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]=12000											
						iValue[sProd.index('BUILDING_WARRENS')]=12001
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				

#Doviello
		if civtype == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize-4) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+15*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+9*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				

#Elohim
		if civtype == gc.getInfoTypeForString('CIVILIZATION_ELOHIM'):
			iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=250
			iValue[sProd.index('BUILDINGCLASS_LIBRARY')]+=200	
			iValue[sProd.index('BUILDINGCLASS_PAGAN_TEMPLE')]+=5000				
			
			iValue[sProd.index('BUILDING_RELIQUARY')]+=20*pCity.getCurrentProductionDifference(False,False)			
			iValue[sProd.index('BUILDING_CHANCEL_OF_GUARDIANS')]+=20*pCity.getCurrentProductionDifference(False,False)
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize+3) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmonk=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MONK'),pCity.area())						
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalarchers+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_MONK')]+=1200+13*(totalunits-totalmonk)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+8*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+10*(totalunits-totalmounted)
						
						iValue[sProd.index('BUILDING_RELIQUARY')]+=4000
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				

#Grigori
		if civtype == gc.getInfoTypeForString('CIVILIZATION_GRIGORI'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=250		
			iValue[sProd.index('BUILDINGCLASS_INN')]+=200
			iValue[sProd.index('BUILDING_ADVENTURERS_GUILD')]+=700			
			iValue[sProd.index('BUILDINGCLASS_TAVERN')]+=30*pCity.getPopulation()
			iValue[sProd.index('BUILDINGCLASS_INFIRMARY')]+=200*pPlayer.getNumCities()/(1+pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_INFIRMARY'))+15*pCity.getPopulation())
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize+2) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						totalpriests=pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_GRIGORI_MEDIC'))
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+15*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+8*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						iValue[sProd.index('UNITCLASS_GRIGORI_MEDIC')]+=1200+10*(totalunits-totalpriests)
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000	
							
						iValue[sProd.index('BUILDING_ADVENTURERS_GUILD')]+=5000									
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_INFIRMARY'))*5:
							iValue[sProd.index('BUILDINGCLASS_INFIRMARY')]=iValue[sProd.index('UNITCLASS_GRIGORI_MEDIC')]+10				

#Hippus
		if civtype == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):
			iValue[sProd.index('BUILDINGCLASS_STABLE')]+=250		
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize-2) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+8*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+11*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+9*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+15*(totalunits-totalmounted)

						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)		
						iValue[sProd.index('BUILDINGCLASS_STABLE')]+=12000									
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				

#Illians
		if civtype == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=100		
			iValue[sProd.index('BUILDINGCLASS_PAGAN_TEMPLE')]+=20*pCity.getCurrentProductionDifference(False,False)+20*pCity.getPopulation()
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize-2) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+15*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+9*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=12000																
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10
							
		if civtype == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
			iValue[sProd.index('BUILDINGCLASS_CATACOMB_LIBRALUS')]=-10000								
							
#Kahzad
		if civtype == gc.getInfoTypeForString('CIVILIZATION_KHAZAD'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=250
			if pCity.isCapital():
				iValue[sProd.index('BUILDINGCLASS_BREWERY')]+=250
			iValue[sProd.index('BUILDINGCLASS_FORGE')]+=400	
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+15*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+11*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=12000																
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				

#Kuriotates
		if civtype == gc.getInfoTypeForString('CIVILIZATION_KURIOTATES'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=-250		
			if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_FINE_CLOTHES'))==0:
				iValue[sProd.index('BUILDING_TAILOR')]+=300
			iValue[sProd.index('BUILDING_TAILOR')]+=200+30*pCity.getPopulation()+30*pCity.getCurrentProductionDifference(False,False)
			if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_JEWELS'))==0:
				iValue[sProd.index('BUILDING_JEWELER')]+=300
			iValue[sProd.index('BUILDING_JEWELER')]+=200+30*pCity.getPopulation()+30*pCity.getCurrentProductionDifference(False,False)
			if pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+8*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+4*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+7*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+11*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+15*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=12000																
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				

#Lanun
		if civtype == gc.getInfoTypeForString('CIVILIZATION_LANUN'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=250		
			iValue[sProd.index('BUILDINGCLASS_HARBOR')]+=100
			if (pCity.isCapital() and pCity.getPopulation>4):
				iValue[sProd.index('BUILDINGCLASS_HERON_THRONE')]+=200
			if pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_WORKBOAT'))<1:
				iValue[sProd.index('UNITCLASS_WORKBOAT')]+=1500		
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+8*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+15*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+9*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=12000																
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				
				
#Ljo
		if civtype == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):
			iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=250		
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize-4) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+13*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+15*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+11*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+-100*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalmages<9:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=12000																
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				

#Luchu
		if civtype == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=1000
			iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]+=pCity.getCurrentProductionDifference(False,False)*8
			iValue[sProd.index('UNITCLASS_ADEPT')]*=1.2			
			iValue[sProd.index('BUILDING_BLASTING_WORKSHOP')]+=400+20*pCity.getCurrentProductionDifference(False,False)		
			iValue[sProd.index('BUILDING_PALLENS_ENGINE')]+=200+20*pCity.getCurrentProductionDifference(False,False)		
			iValue[sProd.index('BUILDING_ADULARIA_CHAMBER')]+=200+20*pCity.getCurrentProductionDifference(False,False)					
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize-4) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+8*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+0*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+15*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+0*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+9*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+0*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<5:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=12000
						iValue[sProd.index('BUILDING_BLASTING_WORKSHOP')]+=12000																						
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				
			
#Malakim
		if civtype == gc.getInfoTypeForString('CIVILIZATION_MALAKIM'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=250		
			iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]+=200
			iValue[sProd.index('BUILDING_CITADEL_OF_LIGHT')]+=200+20*pCity.getCurrentProductionDifference(False,False)
			iValue[sProd.index('BUILDINGCLASS_PAGAN_TEMPLE')]+=100
			iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=250		
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+5*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+10*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+15*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+9*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=12000																
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				
			
#Sheaim	
		if civtype == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
			iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]+=1000
			if pCity.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION)<3:
				iValue[sProd.index('UNITCLASS_GOVANNON')]=19000
				iValue[sProd.index('BUILDINGCLASS_CATACOMB_LIBRALUS')]=3000											
			iValue[sProd.index('BUILDING_PLANAR_GATE')]+=-400*30*pCity.getCurrentProductionDifference(False,False)
			iValue[sProd.index('BUILDINGCLASS_PROPHECY_OF_RAGNAROK')]=2000			
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize-6) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+12*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+10*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+16*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+10*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+0*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)	
						iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]+=12020							
						iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]+=12000																
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				

				
#Sidar
		if civtype == gc.getInfoTypeForString('CIVILIZATION_SIDAR'):
			iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]+=200
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+11*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+10*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+11*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+15*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+11*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)
						iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]+=12000
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10

#Svartalfar
		if civtype == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
			iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]+=250
			if	pPlayer.isConquestMode():
				if pCity.getPopulation()>(iMinCitySize) or (pCity.foodDifference(False)<1):
					if pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif:
						totalmages=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ADEPT'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_MAGE'),pCity.area())
						totalmelee=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_AXEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHAMPION'),pCity.area())
						totalarchers=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_LONGBOWMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_ARCHER'),pCity.area())
						totalrecon=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HUNTER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_RANGER'),pCity.area())
						totalsiege=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CATAPULT'),pCity.area())
						totalmounted=pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSEMAN'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_HORSE_ARCHER'),pCity.area())+pPlayer.getConquestUnitClassCount(gc.getInfoTypeForString('UNITCLASS_CHARIOT'),pCity.area())
				
						totalpriests=0
						if iReli!=-1:
							totalpriests=pPlayer.getConquestUnitClassCount(iReli,pCity.area())
						totalunits=totalmages+totalmelee+totalarchers+totalrecon+totalsiege+totalmounted+totalpriests
						iValue[sProd.index('UNITCLASS_ADEPT')]+=1200+11*(totalunits-totalmages)
						iValue[sProd.index('UNITCLASS_ARCHER')]+=1200+10*(totalunits-totalarchers)
						iValue[sProd.index('UNITCLASS_AXEMAN')]+=1200+11*(totalunits-totalmelee)
						iValue[sProd.index('UNITCLASS_HUNTER')]+=1200+15*(totalunits-totalrecon)
						iValue[sProd.index('UNITCLASS_CATAPULT')]+=1200+11*(totalunits-totalsiege)
						iValue[sProd.index('UNITCLASS_HORSEMAN')]+=1200+12*(totalunits-totalmounted)
						
						if totalsiege<5:
							iValue[sProd.index('UNITCLASS_CATAPULT')]+=2000
						if totalmages<3:
							iValue[sProd.index('UNITCLASS_ADEPT')]+=2000						
						
						if iReli!=-1:
							iValue[sProd.index(sReli)]+=1200+10*(totalunits-totalpriests)						
						iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]+=12000																
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HUNTING_LODGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_HUNTING_LODGE')]=iValue[sProd.index('UNITCLASS_HUNTER')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MAGE_GUILD'))*5:
							iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]=iValue[sProd.index('UNITCLASS_ADEPT')]+10			
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SIEGE_WORKSHOP'))*5:
							iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]=iValue[sProd.index('UNITCLASS_CATAPULT')]+10
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_STABLE'))*5:
							iValue[sProd.index('BUILDINGCLASS_STABLE')]=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10				
						if pPlayer.getNumCities()>pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_ARCHERY_RANGE'))*5:
							iValue[sProd.index('BUILDINGCLASS_ARCHERY_RANGE')]=iValue[sProd.index('UNITCLASS_ARCHER')]+10				
			
			
#Trait specific buildings
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_PHILOSOPHICAL')):
			iValue[sProd.index('BUILDINGCLASS_LIBRARY')]+=400
			iValue[sProd.index('BUILDINGCLASS_ELDER_COUNCIL')]+=400
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_SPIRITUAL')):
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_KILMORPH')]+=200
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_LEAVES')]+=200
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_EMPYREAN')]+=200
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_OVERLORDS')]+=200
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_VEIL')]+=200
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_ORDER')]+=200
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGGRESSIVE')):
			iValue[sProd.index('BUILDINGCLASS_SIEGE_WORKSHOP')]+=200	
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_EXPANSIVE')):
			iValue[sProd.index('BUILDINGCLASS_GRANARY')]+=2000
			iValue[sProd.index('BUILDINGCLASS_HARBOR')]+=2000
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_INDUSTRIOUS')):
			iValue[sProd.index('BUILDINGCLASS_FORGE')]+=200			
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_FINANCIAL')):
			iValue[sProd.index('BUILDINGCLASS_MONEYCHANGER')]+=400
			iValue[sProd.index('BUILDINGCLASS_MARKET')]+=400
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_ARCANE')):
			iValue[sProd.index('BUILDINGCLASS_MAGE_GUILD')]+=200				
			iValue[sProd.index('UNITCLASS_ADEPT')]*=1.2					
		if pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_DEFENDER')):
			iValue[sProd.index('BUILDINGCLASS_PALISADE')]+=200
			iValue[sProd.index('BUILDINGCLASS_WALLS')]+=200			

# general happy buildings
#Civic specific choices
		unhappy=100*(pCity.unhappyLevel(0)+2-pCity.happyLevel())
		if (pCity.unhappyLevel(0)+1)>pCity.happyLevel():
			if pPlayer.getNumCities()>3 or pPlayer.getNumUnits()>20:	#only apply Specialization bonus if Player is well established
				unhappy+=iSpecialization
		if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) == gc.getInfoTypeForString('CIVIC_NATIONHOOD'):
			iValue[sProd.index('BUILDINGCLASS_TRAINING_YARD')]+=200+unhappy

		iValue[sProd.index('BUILDINGCLASS_THEATRE')]+=500+unhappy
		if pPlayer.getCivics(gc.getInfoTypeForString('CIVICOPTION_CULTURAL_VALUES')) == gc.getInfoTypeForString('CIVIC_CONSUMPTION'):
			iValue[sProd.index('BUILDINGCLASS_THEATRE')]+=200
			iValue[sProd.index('BUILDINGCLASS_MARKET')]+=400			
			
		iValue[sProd.index('BUILDINGCLASS_PUBLIC_BATHS')]+=700+unhappy
#				iValue[sProd.index('BUILDINGCLASS_THEATRE')]+=100+unhappy
		iValue[sProd.index('BUILDINGCLASS_BASILICA')]+=100+unhappy
		iValue[sProd.index('BUILDINGCLASS_CARNIVAL')]+=150+unhappy

#Growth Buildings: Granary, Smokehouse 			
		iHealthfactor=(pCity.badHealth(False)-pCity.goodHealth())*200
		if iHealthfactor<0:
			iHealthfactor=0
		iHappyfactor=(pCity.happyLevel()-pCity.unhappyLevel(0))*200
		if iHappyfactor<0:
			iHappyfactor=0
		iValue[sProd.index('BUILDINGCLASS_GRANARY')]+=200+iHealthfactor+iHappyfactor
		iValue[sProd.index('BUILDINGCLASS_SMOKEHOUSE')]+=200+iHealthfactor+iHappyfactor
			
		if iHappyfactor>400 and iHealthfactor>0:
			iValue[sProd.index('BUILDINGCLASS_GRANARY')]+=4000+iSpecialization
			iValue[sProd.index('BUILDINGCLASS_SMOKEHOUSE')]+=4000+iSpecialization

		if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_WHEAT'))>0:
			iValue[sProd.index('BUILDINGCLASS_GRANARY')]+=100
		if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_CORN'))>0:			
			iValue[sProd.index('BUILDINGCLASS_GRANARY')]+=100
		if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_RICE'))>0:							
			iValue[sProd.index('BUILDINGCLASS_GRANARY')]+=100
		if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_SHEEP'))>0:			
			iValue[sProd.index('BUILDINGCLASS_SMOKEHOUSE')]+=100
		if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_PIG'))>0:			
			iValue[sProd.index('BUILDINGCLASS_SMOKEHOUSE')]+=100
		if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_COW'))>0:							
			iValue[sProd.index('BUILDINGCLASS_SMOKEHOUSE')]+=100


		iValue[sProd.index('BUILDING_SMUGGLERS_PORT')]+=750/16*pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_GOLD)
		iValue[sProd.index('BUILDINGCLASS_BASILICA')]+=100*pCity.getMaintenanceTimes100()

#General Building Values
#Commerce Buildings

		iValue[sProd.index('BUILDINGCLASS_ELDER_COUNCIL')]+=700
		if pPlayer.getNumCities()<5:
			iValue[sProd.index('BUILDINGCLASS_ELDER_COUNCIL')]+=15000
		iValue[sProd.index('BUILDINGCLASS_LIBRARY')]+=700/16*pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_RESEARCH)+iSpecialization
		iValue[sProd.index('BUILDINGCLASS_ALCHEMY_LAB')]+=700/36*pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_RESEARCH)+iSpecialization

		if pPlayer.getGold()<500:
			iValue[sProd.index('BUILDINGCLASS_MARKET')]+=900
			if pPlayer.getNumCities()<5:
				iValue[sProd.index('BUILDINGCLASS_MARKET')]+=15000			
			iValue[sProd.index('BUILDINGCLASS_MONEYCHANGER')]+=900/33*pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_GOLD)
			iValue[sProd.index('BUILDINGCLASS_TAX_OFFICE')]+=-200+900/27*pCity.getBaseCommerceRate(CommerceTypes.COMMERCE_GOLD)
			iValue[sProd.index('BUILDINGCLASS_GAMBLING_HOUSE')]+=200+15*pCity.getPopulation()
		iValue[sProd.index('BUILDINGCLASS_HARBOR')]+=100*pCity.getTradeRoutes()
		iValue[sProd.index('BUILDINGCLASS_LIGHTHOUSE')]+=pCity.totalTradeModifier()+50*pCity.getPopulation()
		iValue[sProd.index('BUILDINGCLASS_INN')]+=100*pCity.getTradeRoutes()+pCity.totalTradeModifier()
		iValue[sProd.index('BUILDINGCLASS_TAVERN')]+=110*pCity.getTradeRoutes()+pCity.totalTradeModifier()
		
		iValue[sProd.index('BUILDINGCLASS_COURTHOUSE')]+=pCity.getMaintenanceTimes100()
		iValue[sProd.index('BUILDINGCLASS_DUNGEON')]+=200*pCity.getWarWearinessModifier()		
#Production Buildings
		iValue[sProd.index('BUILDINGCLASS_FORGE')]+=60*pCity.getCurrentProductionDifference(False,False)+iSpecialization		
		if pCity.getCurrentProductionDifference(False,False)>15:		
			iValue[sProd.index('BUILDINGCLASS_FORGE')]+=2000
			if pPlayer.isConquestMode():
				iValue[sProd.index('BUILDINGCLASS_FORGE')]+=10000				
			iValue[sProd.index('BUILDING_COMMAND_POST')]+=250+15*pCity.getCurrentProductionDifference(False,False)				
			if pPlayer.isConquestMode():			
				iValue[sProd.index('BUILDING_COMMAND_POST')]+=10000
			
#Defense Buildings
		iValue[sProd.index('BUILDINGCLASS_PALISADE')]+=250+15*pCity.getPopulation()		
		iValue[sProd.index('BUILDINGCLASS_WALLS')]+=200+15*pCity.getPopulation()
#Religion Buildings

#Wonders and Rituals
		iwondermod=2000
		iconquestmod=0
		if	(pPlayer.isConquestMode() and (pPlayer.countGroupFlagUnits(10)<pPlayer.getNumCities()*iDif)):
			iconquestmod=-2000

		if (pPlayer.getNumCities()>3):
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_BREWERY'))==0:
				iValue[sProd.index('BUILDINGCLASS_BREWERY')]+=250+15*pCity.getCurrentProductionDifference(False,False)	
		if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HERON_THRONE'))==0:				
			iValue[sProd.index('BUILDINGCLASS_HERON_THRONE')]+=250+15*pCity.getPopulation()
			if pCity.isCoastal(10):
				if pPlayer.getNumCities()>2:
					iValue[sProd.index('BUILDINGCLASS_HERON_THRONE')]+=1000			
		if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_GREAT_LIGHTHOUSE'))==0:
			iValue[sProd.index('BUILDINGCLASS_GREAT_LIGHTHOUSE')]+=250+15*pCity.getPopulation()
		if pPlayer.getFavoriteReligion()==gc.getInfoTypeForString('RELIGION_THE_ORDER'):
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MERCURIAN_GATE'))==0:
				iValue[sProd.index('BUILDINGCLASS_MERCURIAN_GATE')]+=iwondermod
		if pCity.getMaintenanceTimes100()>600:
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_FORBIDDEN_PALACE'))==0:
				iValue[sProd.index('BUILDINGCLASS_FORBIDDEN_PALACE')]+=iwondermod+iconquestmod
		if pCity.findCommerceRateRank(CommerceTypes.COMMERCE_RESEARCH)<3:
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_CROWN_OF_AKHARIEN'))==0:
				iValue[sProd.index('BUILDINGCLASS_CROWN_OF_AKHARIEN')]+=iwondermod+iconquestmod
		if pCity.findCommerceRateRank(CommerceTypes.COMMERCE_GOLD)==1:
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_BAZAAR_OF_MAMMON'))==0:
				iValue[sProd.index('BUILDINGCLASS_BAZAAR_OF_MAMMON')]+=iwondermod+iconquestmod
				if pCity.isHolyCity():
					iValue[sProd.index('BUILDINGCLASS_BAZAAR_OF_MAMMON')]+=2000
		if pCity.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION)<3:
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_GUILD_OF_THE_NINE'))==0:
				iValue[sProd.index('BUILDINGCLASS_GUILD_OF_THE_NINE')]+=0 # iwondermod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_CITY_OF_A_THOUSAND_SLUMS'))==0:
				iValue[sProd.index('BUILDINGCLASS_CITY_OF_A_THOUSAND_SLUMS')]+=0 # iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_THEATRE_OF_DREAMS'))==0:
				iValue[sProd.index('BUILDINGCLASS_THEATRE_OF_DREAMS')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_PILLAR_OF_CHAINS'))==0:
				iValue[sProd.index('BUILDINGCLASS_PILLAR_OF_CHAINS')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_GUILD_OF_HAMMERS'))==0:
				iValue[sProd.index('BUILDINGCLASS_GUILD_OF_HAMMERS')]+=iwondermod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_GRAND_MENAGERIE'))==0:
				iValue[sProd.index('BUILDINGCLASS_GRAND_MENAGERIE')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_CELESTIAL_COMPASS'))==0:
				iValue[sProd.index('BUILDINGCLASS_CELESTIAL_COMPASS')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_RIDE_OF_THE_NINE_KINGS'))==0:
				iValue[sProd.index('BUILDINGCLASS_RIDE_OF_THE_NINE_KINGS')]+=iwondermod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MOKKAS_CAULDRON'))==0:
				iValue[sProd.index('BUILDINGCLASS_MOKKAS_CAULDRON')]+=0
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SHRINE_OF_SIRONA'))==0:
				iValue[sProd.index('BUILDINGCLASS_SHRINE_OF_SIRONA')]+=0 # iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_EYES_AND_EARS_NETWORK'))==0:
				iValue[sProd.index('BUILDINGCLASS_EYES_AND_EARS_NETWORK')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SHRINE_OF_THE_CHAMPION'))==0:
				iValue[sProd.index('BUILDINGCLASS_SHRINE_OF_THE_CHAMPION')]+=iwondermod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_AQUAE_SUCELLUS'))==0:
				iValue[sProd.index('BUILDINGCLASS_AQUAE_SUCELLUS')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_HALL_OF_KINGS'))==0:
				iValue[sProd.index('BUILDINGCLASS_HALL_OF_KINGS')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_GREAT_LIBRARY'))==0:
				iValue[sProd.index('BUILDINGCLASS_GREAT_LIBRARY')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_TEMPORENCE'))==0:
				iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_TEMPORENCE')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TEMPLE_OF_TEMPORENCE'))==0:
				iValue[sProd.index('BUILDINGCLASS_HEROIC_EPIC')]+=iwondermod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_NATIONAL_EPIC'))==0:
				iValue[sProd.index('BUILDINGCLASS_NATIONAL_EPIC')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_COMPLACENCY'))==0:
				iValue[sProd.index('BUILDINGCLASS_TOWER_OF_COMPLACENCY')]+=iwondermod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_EYES'))==0:
				iValue[sProd.index('BUILDINGCLASS_TOWER_OF_EYES')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_SYLIVENS_PERFECT_LYRE'))==0:
				iValue[sProd.index('BUILDINGCLASS_SYLIVENS_PERFECT_LYRE')]+=iwondermod+iconquestmod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_CATACOMB_LIBRALUS'))==0:
				iValue[sProd.index('BUILDINGCLASS_CATACOMB_LIBRALUS')]+=0
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_FORM_OF_THE_TITAN'))==0:
				iValue[sProd.index('BUILDINGCLASS_FORM_OF_THE_TITAN')]+=iwondermod
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_MINES_OF_GALDUR'))==0:
				iValue[sProd.index('BUILDINGCLASS_MINES_OF_GALDUR')]+=iwondermod
				
			iValue[sProd.index('PROJECT_BLOOD_OF_THE_PHOENIX')]+=iwondermod
			iValue[sProd.index('PROJECT_BIRTHRIGHT_REGAINED')]+=iwondermod			
			
			if pPlayer.getNumCities()>10:
				iValue[sProd.index('PROJECT_GENESIS')]+=iwondermod			
			iValue[sProd.index('PROJECT_NATURES_REVOLT')]+=iwondermod
			if civtype == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO'):			
				iValue[sProd.index('PROJECT_NATURES_REVOLT')]+=10000
			if civtype == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):			
				iValue[sProd.index('PROJECT_NATURES_REVOLT')]+=10000
			if civtype == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):			
				iValue[sProd.index('PROJECT_NATURES_REVOLT')]+=10000
			
			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isReligionVictory():			
				if pPlayer.getStateReligion()==pPlayer.getFavoriteReligion() and pPlayer.isConquestMode():
					iValue[sProd.index('PROJECT_PURGE_THE_UNFAITHFUL')]=17000									

			if pPlayer.getNumCities()>3:			
				iValue[sProd.index('PROJECT_SAMHAIN')]+=17000			
			if pPlayer.getNumCities()>5:			
				iValue[sProd.index('PROJECT_THE_WHITE_HAND')]+=17000
			if pPlayer.getNumCities()>5:			
				iValue[sProd.index('PROJECT_THE_DEEPENING')]+=17000
			iValue[sProd.index('PROJECT_STIR_FROM_SLUMBER')]=17000
			iValue[sProd.index('PROJECT_THE_DRAW')]=17000			
			iValue[sProd.index('PROJECT_ASCENSION')]=17000				
				
			if civtype == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):			
				iValue[sProd.index('PROJECT_PACT_OF_THE_NILHORN')]+=10000
			if civtype == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):			
				iValue[sProd.index('PROJECT_PACT_OF_THE_NILHORN')]+=10000				
		
#Buildings only for Big Cities
		iValue[sProd.index('BUILDINGCLASS_AQUEDUCT')]+=15*pCity.getPopulation()
		iValue[sProd.index('BUILDINGCLASS_GROVE')]+=15*pCity.getPopulation()
		iValue[sProd.index('BUILDINGCLASS_HERBALIST')]+=150+5*pCity.getPopulation()

#Victory Conditions

#Altar Victory

		iValue[sProd.index('BUILDINGCLASS_ALTAR_OF_THE_LUONNOTAR_FINAL')]=35000

#Arcane Tower Victory
		if pCity.findBaseYieldRateRank(YieldTypes.YIELD_PRODUCTION)<3:
			if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isArcaneTowerVictory():
				iValue[sProd.index('PROJECT_RITES_OF_OGHMA')]=17000					
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_ALTERATION'))==0:					
				iValue[sProd.index('BUILDINGCLASS_TOWER_OF_ALTERATION')]=17000
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_DIVINATION'))==0:									
				iValue[sProd.index('BUILDINGCLASS_TOWER_OF_DIVINATION')]=17000
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'))==0:								
				iValue[sProd.index('BUILDINGCLASS_TOWER_OF_NECROMANCY')]=17000
			if pPlayer.getBuildingClassCountPlusMaking(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS'))==0:								
				iValue[sProd.index('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS')]=17000
			iValue[sProd.index('BUILDINGCLASS_TOWER_OF_MASTERY')]=35000

#Culture Victory
		bCultureImportant=false		
		if ((gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isCultureVictory() and pPlayer.isConquestMode()) and pCity.findCommerceRateRank(CommerceTypes.COMMERCE_CULTURE)<6):
			bCultureImportant=true
		if pCity.calculateCulturePercent(ePlayer)<65:
			bCultureImportant=true
		if bCultureImportant:
			iValue[sProd.index('BUILDINGCLASS_CARNIVAL')]+=2000
			iValue[sProd.index('BUILDINGCLASS_GROVE')]+=2000
			iValue[sProd.index('BUILDINGCLASS_INN')]+=2000
			iValue[sProd.index('BUILDINGCLASS_LIBRARY')]+=2000
			iValue[sProd.index('BUILDINGCLASS_MONUMENT')]+=2000
			iValue[sProd.index('BUILDINGCLASS_PAGAN_TEMPLE')]+=2000
			iValue[sProd.index('BUILDINGCLASS_TAVERN')]+=2000
			iValue[sProd.index('BUILDINGCLASS_THEATRE')]+=2000
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_LEAVES')]+=2000
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_KILMORPH')]+=2000
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_EMPYREAN')]+=2000
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_OVERLORDS')]+=2000
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_VEIL')]+=2000
			iValue[sProd.index('BUILDINGCLASS_TEMPLE_OF_THE_ORDER')]+=2000

#Religion Victory			
		if gc.getLeaderHeadInfo(pPlayer.getLeaderType()).isReligionVictory():
			if not (pPlayer.hasTrait(gc.getInfoTypeForString('TRAIT_AGNOSTIC'))):		
				ireligion=pPlayer.getStateReligion()
				if ireligion==pPlayer.getFavoriteReligion():			
					if pPlayer.countGroupFlagUnits(15)<(pPlayer.getNumCities()/5):
						if iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_VEIL')]<4000: 
							iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_VEIL')]=4000
						if iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_ORDER')]<4000: 
							iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_ORDER')]=4000
						if iValue[sProd.index('UNITCLASS_PRIEST_OF_KILMORPH')]<4000: 
							iValue[sProd.index('UNITCLASS_PRIEST_OF_KILMORPH')]=4000
						if iValue[sProd.index('UNITCLASS_PRIEST_OF_LEAVES')]<4000: 
							iValue[sProd.index('UNITCLASS_PRIEST_OF_LEAVES')]=4000
						if iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_EMPYREAN')]<4000: 
							iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_EMPYREAN')]=4000
						if iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_OVERLORDS')]<4000: 
							iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_OVERLORDS')]=4000

					
#Value higher Tier units more

		if (iValue[sProd.index('UNITCLASS_WARRIOR')]>iValue[sProd.index('UNITCLASS_AXEMAN')]):
			iValue[sProd.index('UNITCLASS_AXEMAN')]=iValue[sProd.index('UNITCLASS_WARRIOR')]+2		
		if (iValue[sProd.index('UNITCLASS_WARRIOR')]>iValue[sProd.index('UNITCLASS_ARCHER')]):
			iValue[sProd.index('UNITCLASS_ARCHER')]=iValue[sProd.index('UNITCLASS_WARRIOR')]+2		
		if (iValue[sProd.index('UNITCLASS_WARRIOR')]>iValue[sProd.index('UNITCLASS_HUNTER')]):
			iValue[sProd.index('UNITCLASS_HUNTER')]=iValue[sProd.index('UNITCLASS_WARRIOR')]+2		

		if (iValue[sProd.index('UNITCLASS_AXEMAN')]>0):							
			iValue[sProd.index('UNITCLASS_CHAMPION')]+=iValue[sProd.index('UNITCLASS_AXEMAN')]+10

		if iValue[sProd.index('UNITCLASS_ARCHER')]>0:							
			iValue[sProd.index('UNITCLASS_LONGBOWMAN')]+=iValue[sProd.index('UNITCLASS_ARCHER')]+10

		if iValue[sProd.index('UNITCLASS_HUNTER')]>0:							
			iValue[sProd.index('UNITCLASS_RANGER')]+=iValue[sProd.index('UNITCLASS_HUNTER')]+10+pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_ASSASSIN'))																	
			iValue[sProd.index('UNITCLASS_ASSASSIN')]+=iValue[sProd.index('UNITCLASS_HUNTER')]+10+pPlayer.getUnitClassCountPlusMaking(gc.getInfoTypeForString('UNITCLASS_RANGER'))																	

		if iValue[sProd.index('UNITCLASS_HORSEMAN')]>0:							
			iValue[sProd.index('UNITCLASS_CHARIOT')]+=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10
			iValue[sProd.index('UNITCLASS_HORSE_ARCHER')]+=iValue[sProd.index('UNITCLASS_HORSEMAN')]+10
			
		if iValue[sProd.index('UNITCLASS_CATAPULT')]>0:										
			iValue[sProd.index('UNITCLASS_CANNON')]+=iValue[sProd.index('UNITCLASS_CATAPULT')]+5		
			iValue[sProd.index('UNITCLASS_PRIEST_OF_THE_VEIL')]+=iValue[sProd.index('UNITCLASS_CATAPULT')]+10		
			
		infoCiv = gc.getCivilizationInfo(civtype)		
		iBestBuilding=-1
		iBestBuildingValue=0
		for i in range(len(sProd)):
			if iValue[i]>iBestBuildingValue:
				if iValue[i]>iBuildingthres:
					if iProdType[i]==0:				
						if pCity.canConstruct(gc.getInfoTypeForString(sProd[i]),True,False,False):
							iBestBuildingValue=iValue[i]
							iBestBuilding=i
					elif iProdType[i]==1:
						iBuilding = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString(sProd[i]))				
						if iBuilding != -1:
							if pCity.canConstruct(iBuilding,True,False,False):
								iBestBuildingValue=iValue[i]
								iBestBuilding=i						
					elif iProdType[i]==2:
						iUnit = infoCiv.getCivilizationUnits(gc.getInfoTypeForString(sProd[i]))
						if iUnit != -1:
							if pCity.canTrain(iUnit,True,False):
								iBestBuildingValue=iValue[i]
								iBestBuilding=i
					elif iProdType[i]==3:								
						if pCity.canCreate(gc.getInfoTypeForString(sProd[i]),True,False):
							iBestBuildingValue=iValue[i]
							iBestBuilding=i
					

#		if ePlayer==0:
#		CyInterface().addMessage(0,true,25,"This is City %s: Our best Building is (%s), Value (%s). Threshold is (%s)!" %(pCity.getName(),sProd[iBestBuilding],iValue[iBestBuilding],iBuildingthres),'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)


#		if	pPlayer.isConquestMode():
#			CyInterface().addMessage(0,true,25,"This is City %s: Our best Building is (%s), Value (%s). Threshold is (%s)!" %(pCity.getName(),sProd[iBestBuilding],iValue[iBestBuilding],iBuildingthres),'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)
#		if civtype == gc.getInfoTypeForString('CIVILIZATION_AMURITES'):
#			CyInterface().addMessage(0,true,25,"This is City %s: Our best Building is (%s), Value (%s). Threshold is (%s)!" %(pCity.getName(),sProd[iBestBuilding],iValue[iBestBuilding],iBuildingthres),'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)
#		if ePlayer==0:
#			CyInterface().addMessage(0,true,25,"We need this many Mages: %s !" %(cf.calculateMagesNeeded(ePlayer)),'',0,'',ColorTypes(11), pPlot.getX(), pPlot.getY(), True,True)	

		if iBestBuilding!=-1:
			if iProdType[iBestBuilding]==0:
				pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,gc.getInfoTypeForString(sProd[iBestBuilding]),-1, False, False, False, False)				
				return 1
			elif iProdType[iBestBuilding]==1:
				iBuilding = infoCiv.getCivilizationBuildings(gc.getInfoTypeForString(sProd[iBestBuilding]))
				pCity.pushOrder(OrderTypes.ORDER_CONSTRUCT,iBuilding,-1, False, False, False, False)					
				return 1					
			elif iProdType[iBestBuilding]==2:
				iUnit = infoCiv.getCivilizationUnits(gc.getInfoTypeForString(sProd[iBestBuilding]))
				pCity.pushOrder(OrderTypes.ORDER_TRAIN,iUnit,-1, False, False, False, False)
				return 1
			elif iProdType[iBestBuilding]==3:
				pCity.pushOrder(OrderTypes.ORDER_CREATE,gc.getInfoTypeForString(sProd[iBestBuilding]),-1, False, False, False, False)
				return 1				

		return False

	def AI_unitUpdate(self,argsList):
		pUnit = argsList[0]
		pPlot = pUnit.plot()
							
		if pUnit.getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_GIANT_SPIDER'):
			iX = pUnit.getX()
			iY = pUnit.getY()
			for iiX in range(iX-1, iX+2, 1):
				for iiY in range(iY-1, iY+2, 1):
					pLoopPlot = CyMap().plot(iiX,iiY)
					for i in range(pLoopPlot.getNumUnits()):
						if pLoopPlot.getUnit(i).getOwner() != pUnit.getOwner():
							return 0
			pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
			return 1
		
		iImprovement = pPlot.getImprovementType()
		if iImprovement != -1:
			if (iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BARROW') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_RUINS') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_HELLFIRE')):
				if not pUnit.isAnimal():
					if pPlot.getNumUnits() - pPlot.getNumAnimalUnits() == 1:
						pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
						return 1
			if (iImprovement == gc.getInfoTypeForString('IMPROVEMENT_BEAR_DEN') or iImprovement == gc.getInfoTypeForString('IMPROVEMENT_LION_DEN')):
				if pUnit.isAnimal():
					if pPlot.getNumAnimalUnits() == 1:
						pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
						return 1
			if iImprovement == gc.getInfoTypeForString('IMPROVEMENT_GOBLIN_FORT'):
				if pUnit.getUnitCombatType() == gc.getInfoTypeForString('UNITCOMBAT_ARCHER'):
					pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
					return 1
				if not pUnit.isAnimal():
					if pPlot.getNumUnits() - pPlot.getNumAnimalUnits() <= 2:
						pUnit.getGroup().pushMission(MissionTypes.MISSION_SKIP, 0, 0, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
						return 1
		
		return False

	def AI_doWar(self,argsList):
		eTeam = argsList[0]
		return False

	def AI_doDiplo(self,argsList):
		ePlayer = argsList[0]
		return False

	def calculateScore(self,argsList):
		ePlayer = argsList[0]
		bFinal = argsList[1]
		bVictory = argsList[2]
		
		iPopulationScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getPopScore(), gc.getGame().getInitPopulation(), gc.getGame().getMaxPopulation(), gc.getDefineINT("SCORE_POPULATION_FACTOR"), True, bFinal, bVictory)
		iLandScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getLandScore(), gc.getGame().getInitLand(), gc.getGame().getMaxLand(), gc.getDefineINT("SCORE_LAND_FACTOR"), True, bFinal, bVictory)
		iTechScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getTechScore(), gc.getGame().getInitTech(), gc.getGame().getMaxTech(), gc.getDefineINT("SCORE_TECH_FACTOR"), True, bFinal, bVictory)
		iWondersScore = CvUtil.getScoreComponent(gc.getPlayer(ePlayer).getWondersScore(), gc.getGame().getInitWonders(), gc.getGame().getMaxWonders(), gc.getDefineINT("SCORE_WONDER_FACTOR"), False, bFinal, bVictory)
		return int(iPopulationScore + iLandScore + iWondersScore + iTechScore)

	def doHolyCity(self):
		return False

	def doHolyCityTech(self,argsList):
		eTeam = argsList[0]
		ePlayer = argsList[1]
		eTech = argsList[2]
		bFirst = argsList[3]
		return False

	def doGold(self,argsList):
		ePlayer = argsList[0]
		return False

	def doResearch(self,argsList):
		ePlayer = argsList[0]
		return False

	def doGoody(self,argsList):
		ePlayer = argsList[0]
		pPlot = argsList[1]
		pUnit = argsList[2]
		return False

	def doGrowth(self,argsList):
		pCity = argsList[0]
		return False

	def doProduction(self,argsList):
		pCity = argsList[0]
		return False

	def doCulture(self,argsList):
		pCity = argsList[0]
		return False

	def doPlotCulture(self,argsList):
		pCity = argsList[0]
		bUpdate = argsList[1]
		ePlayer = argsList[2]
		iCultureRate = argsList[3]
		return False

	def doReligion(self,argsList):
		pCity = argsList[0]
		return False

	def cannotSpreadReligion(self,argsList):
		iOwner, iUnitID, iReligion, iX, iY = argsList[0]
		return False

	def doGreatPeople(self,argsList):
		pCity = argsList[0]
		return False

	def doMeltdown(self,argsList):
		pCity = argsList[0]
		return False
	
	def doReviveActivePlayer(self,argsList):
		"allows you to perform an action after an AIAutoPlay"
		iPlayer = argsList[0]
		return False
	
	def doPillageGold(self, argsList):
		"controls the gold result of pillaging"
		pPlot = argsList[0]
		pUnit = argsList[1]
		
		iPillageGold = 0
		iPillageGold = CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 1")
		iPillageGold += CyGame().getSorenRandNum(gc.getImprovementInfo(pPlot.getImprovementType()).getPillageGold(), "Pillage Gold 2")

		iPillageGold += (pUnit.getPillageChange() * iPillageGold) / 100
		
		return iPillageGold
	
	def doCityCaptureGold(self, argsList):
		"controls the gold result of capturing a city"
		
		pOldCity = argsList[0]
		
		iCaptureGold = 0
		
		iCaptureGold += gc.getDefineINT("BASE_CAPTURE_GOLD")
		iCaptureGold += (pOldCity.getPopulation() * gc.getDefineINT("CAPTURE_GOLD_PER_POPULATION"))
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND1"), "Capture Gold 1")
		iCaptureGold += CyGame().getSorenRandNum(gc.getDefineINT("CAPTURE_GOLD_RAND2"), "Capture Gold 2")

		if (gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS") > 0):
			iCaptureGold *= cyIntRange((CyGame().getGameTurn() - pOldCity.getGameTurnAcquired()), 0, gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS"))
			iCaptureGold /= gc.getDefineINT("CAPTURE_GOLD_MAX_TURNS")
		
		return iCaptureGold
	
	def citiesDestroyFeatures(self,argsList):
		iX, iY= argsList
		return True
		
	def canFoundCitiesOnWater(self,argsList):
		iX, iY= argsList

		pPlot = CyMap().plot(iX,iY)
		for i in range(pPlot.getNumUnits()):
			if pPlot.getUnit(i).getUnitClassType() == gc.getInfoTypeForString('UNITCLASS_HIGH_PRIEST_OF_THE_OVERLORDS'):
				return True
		return False
		
	def doCombat(self,argsList):
		pSelectionGroup, pDestPlot = argsList
		return False

	def getConscriptUnitType(self, argsList):
		iPlayer = argsList[0]
		iConscriptUnitType = -1 #return this with the value of the UNIT TYPE you want to be conscripted, -1 uses default system
		
		return iConscriptUnitType

	def getCityFoundValue(self, argsList):
		iPlayer, iPlotX, iPlotY = argsList
		iFoundValue = -1 # Any value besides -1 will be used
		
		return iFoundValue
		
	def canPickPlot(self, argsList):
		pPlot = argsList[0]
		return true
		
	def getUnitCostMod(self, argsList):
		iPlayer, iUnit = argsList
		iCostMod = -1 # Any value > 0 will be used
		
		return iCostMod

	def getBuildingCostMod(self, argsList):
		iPlayer, iCityID, iBuilding = argsList
		pPlayer = gc.getPlayer(iPlayer)
		pCity = pPlayer.getCity(iCityID)

		iCostMod = -1 # Any value > 0 will be used

		if iBuilding == gc.getInfoTypeForString('BUILDING_GAMBLING_HOUSE'):
			if pPlayer.isGamblingRing():
				iCostMod = gc.getBuildingInfo(iBuilding).getProductionCost() / 4
		
		return iCostMod
		
	def canUpgradeAnywhere(self, argsList):
		pUnit = argsList
		
		bCanUpgradeAnywhere = 0
		
		return bCanUpgradeAnywhere
		
	def getWidgetHelp(self, argsList):
		eWidgetType, iData1, iData2, bOption = argsList
		
		return u""
		
	def getUpgradePriceOverride(self, argsList):
		iPlayer, iUnitID, iUnitTypeUpgrade = argsList
		
		return -1	# Any value 0 or above will be used
	
	def getExperienceNeeded(self, argsList):
		# use this function to set how much experience a unit needs
		iLevel, iOwner = argsList
		
		iExperienceNeeded = 0

		# regular epic game experience		
		iExperienceNeeded = iLevel * iLevel + 1

		iModifier = gc.getPlayer(iOwner).getLevelExperienceModifier()
		if (0 != iModifier):
			iExperienceNeeded += (iExperienceNeeded * iModifier + 99) / 100   # ROUND UP
			
		return iExperienceNeeded
		
# Return 1 if a Mission was pushed
	def AI_MageTurn(self, argsList):
		pUnit = argsList[0]
		pPlot = pUnit.plot()
		pPlayer = gc.getPlayer(pUnit.getOwner())
		eTeam = gc.getTeam(pPlayer.getTeam())
		iCiv = pPlayer.getCivilizationType()
		iX = pUnit.getX()
		iY = pUnit.getY()
		
		if (pUnit.getUnitAIType() == gc.getInfoTypeForString('UNITAI_TERRAFORMER')):

#-----------------------------------
#TERRAFORMING
#
#SETTING FLAGS
#
#-----------------------------------

			searchdistance=3

#-----------------------------------
#SETTING FLAGS
#
#INIT
#CIV SPECIFIC
#UNIT SPECIFIC
#-----------------------------------

#INIT
			smokeb = true #terraformer tries to put out smoke
			desertb = true #terraformer tries to spring deserts
			snowb = true #terraformer tries to scorch snow to tundra
			tundrab = true #terraformer tries to scorch tundra to plains
			marshb = true #terraformer tries to scorch marsh to grassland
			grassb = false #terraformer tries to scorch grassland to plains			
			hellterrb = true #terraformer tries to remove hell terrain
			treesb = false #terraformer tries to Create Trees
			canupgrademana = false #terraformer tries to upgrade mana nodes

			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):			
				canupgrademana=true
			elif pPlayer.isHasTech(gc.getInfoTypeForString('TECH_ALTERATION')):
				canupgrademana=true			
			elif pPlayer.isHasTech(gc.getInfoTypeForString('TECH_DIVINATION')):
				canupgrademana=true			
			elif pPlayer.isHasTech(gc.getInfoTypeForString('TECH_ELEMENTALISM')):
				canupgrademana=true			
			elif pPlayer.isHasTech(gc.getInfoTypeForString('TECH_NECROMANCY')):
				canupgrademana=true			
								
			rawmana = 0
			desert = 0
			snow = 0
			tundra = 0
			marsh = 0
			grass = 0
			hellterr = 0
			floodplain = 0
			trees = 0

#CIV SPECIFICS			
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				smokeb = false
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):
				desertb = false
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_ILLIANS'):
				snowb = false
			if (iCiv == gc.getInfoTypeForString('CIVILIZATION_DOVIELLO') or iCiv == gc.getInfoTypeForString('CIVILIZATION_ILLIANS')):
				tundrab = false	
			if iCiv == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				hellterrb = false
				
#UNIT SPECIFIC
			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_DEVOUT'):			
				desertb = false #terraformer tries to spring deserts
				snowb = false #terraformer tries to scorch snow to tundra
				tundrab = false #terraformer tries to scorch tundra to plains
				marshb = false #terraformer tries to scorch marsh to grassland
				grassb = false #terraformer tries to scorch grassland to plains			
				hellterrb = true #terraformer tries to remove hell terrain
				treesb = false #terraformer tries to Create Trees				
				treesimpb= false #terraformer can Create Trees in Improvements				
				canupgrademana = false #terraformer tries to upgrade mana nodes

			if pUnit.getUnitType() == gc.getInfoTypeForString('UNIT_PRIEST_OF_LEAVES'):
				desertb = false #terraformer tries to spring deserts
				snowb = false #terraformer tries to scorch snow to tundra
				tundrab = false #terraformer tries to scorch tundra to plains
				marshb = false #terraformer tries to scorch marsh to grassland
				grassb = false #terraformer tries to scorch grassland to plains			
				hellterrb = false #terraformer tries to remove hell terrain				
				treesb = true #terraformer tries to Create Trees			
				treesimpb = false
				if (iCiv == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR') or iCiv == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR')):
					treesimpb = true
				if ((treesimpb == False) and (pPlayer.getStateReligion() != gc.getInfoTypeForString('RELIGION_FELLOWSHIP_OF_LEAVES'))):
					if not pPlayer.isHuman():
						pUnit.setUnitAIType(gc.getInfoTypeForString('UNITAI_RESERVE'))
						return 0
					
				canupgrademana = false #terraformer tries to upgrade mana nodes
				
#prefer to upgrade mana rather than terraform?
			if canupgrademana:
				if CyGame().getSorenRandNum(100, "Upgrademana")<10:
					pUnit.setUnitAIType(gc.getInfoTypeForString('UNITAI_MANA_UPGRADE'))
					return 0
				if (pPlayer.getArcaneTowerVictoryFlag()>0):
					pUnit.setUnitAIType(gc.getInfoTypeForString('UNITAI_MANA_UPGRADE'))
					return 0
				
#-----------------------------------
#TERRAFORMING
#
#MALAKIM EXCEPTION
#TERRAFORMING
#-----------------------------------


#TERRAFORMING
			if pPlot.getOwner()==pUnit.getOwner():
				if (desertb or pPlot.isRiver()):
					if pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_DESERT'):
						if pUnit.canCast(gc.getInfoTypeForString('SPELL_SPRING'),false):
							pUnit.cast(gc.getInfoTypeForString('SPELL_SPRING'))
							return 0
				elif smokeb:
					if pPlot.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SMOKE'):
						if pUnit.canCast(gc.getInfoTypeForString('SPELL_SPRING'),false):
							pUnit.cast(gc.getInfoTypeForString('SPELL_SPRING'))
							return 0

				if (snowb and pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_SNOW')):
					if pUnit.canCast(gc.getInfoTypeForString('SPELL_SCORCH'),false):
						pUnit.cast(gc.getInfoTypeForString('SPELL_SCORCH'))
						return 0

				if (tundrab and pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_TUNDRA')):
					if pUnit.canCast(gc.getInfoTypeForString('SPELL_SCORCH'),false):
						pUnit.cast(gc.getInfoTypeForString('SPELL_SCORCH'))
						return 0

				if (marshb and pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_MARSH')):
					if pUnit.canCast(gc.getInfoTypeForString('SPELL_SCORCH'),false):
						pUnit.cast(gc.getInfoTypeForString('SPELL_SCORCH'))
						return 0

				if (grassb and pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_GRASS')):
					if pUnit.canCast(gc.getInfoTypeForString('SPELL_SCORCH'),false):
						pUnit.cast(gc.getInfoTypeForString('SPELL_SCORCH'))
						return 0

				if hellterrb:
					if pUnit.canCast(gc.getInfoTypeForString('SPELL_SANCTIFY'),false):
						pUnit.cast(gc.getInfoTypeForString('SPELL_SANCTIFY'))
						return 0

				if treesb:
					if pPlot.getFeatureType()==-1:
						if pUnit.canCast(gc.getInfoTypeForString('SPELL_BLOOM'),false):
							pUnit.cast(gc.getInfoTypeForString('SPELL_BLOOM'))
							return 0

#-----------------------------------
#LOOK FOR WORK
#
#MALAKIM EXCEPTION
#LOOK FOR WORK
#-----------------------------------


			for isearch in range(1,searchdistance,1):
								
	#LOOK FOR WORK			
				if 1==1:
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():
									if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
										if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1')):
											if smokeb:
												if (pPlot2.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SMOKE')):
													desert=desert+1
											if (desertb or pPlot.isRiver()):
												if (pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_DESERT') and not pPlot2.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')):
													if not pPlot2.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):
														desert=desert+1
										if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN1')):
											if snowb:
												if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_SNOW'):
													snow=snow+1								
											if tundrab:
												if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_TUNDRA'):
													tundra=tundra+1								
											if marshb:
												if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_MARSH'):
													marsh=marsh+1								
											if grassb:
												if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_GRASS'):
													grass=grass+1
										if hellterrb:								
											if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE1')):
												if (pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BROKEN_LANDS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BURNING_SANDS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SHALLOWS')):
													hellterr=hellterr+1													
										if treesb:
											if (pPlot2.getFeatureType() == -1):
												if (pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_GRASS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA')):
													if not pPlot2.isCity():
														if (pPlot2.getImprovementType()==-1 or treesimpb):
															trees=trees+1
										
	#Remove some deserts/smoke etc.?			

				if desert>0:
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):			
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():
									if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
										if smokeb:
											if (pPlot2.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SMOKE')):
												pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
												return 1
										if (desertb or pPlot.isRiver()):
											if (pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_DESERT') and not pPlot2.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')):
												if not pPlot2.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):											
													pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
													return 1


				if snow>0:
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):			
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():						
									if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
										if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_SNOW'):
											pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
											return 1

				if tundra>0:
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):			
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():						
									if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
										if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_TUNDRA'):
											pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
											return 1
				if marsh>0:
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):			
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():						
									if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
										if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_MARSH'):
											pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
											return 1

				if grass>0:
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):			
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():						
									if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
										if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_GRASS'):
											pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
											return 1
																																												

	#Hell terrain to sanctify?
				if (hellterr>0 and pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE1'))):
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner()) or pPlot2.isWater()):
								if pPlot2.getOwner()==pUnit.getOwner():								
									if gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_PLOT_COUNTER):
										if (pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BROKEN_LANDS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BURNING_SANDS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SHALLOWS')):
											pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)																	
									elif pPlot2.getPlotCounter()>7:
										pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
			
				if floodplain>0:
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):			
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():						
									if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
										if (pPlot2.isRiver() and pPlot2.getFeatureType()==-1):
											pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
											return 1

				if trees>0:
					for iiX in range(iX-isearch, iX+isearch+1, 1):
						for iiY in range(iY-isearch, iY+isearch+1, 1):			
							pPlot2 = CyMap().plot(iiX,iiY)
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():						
									if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
										if (pPlot2.getFeatureType() == -1):
											if (pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_GRASS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA')):										
												if not pPlot2.isCity():
													if (pPlot2.getImprovementType()==-1 or treesimpb):										
														pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)							
														return 1											
			
#Nothing to do, lets move on to another City!
#			chance = CyGame().getSorenRandNum(pPlayer.getNumCities(), "MOVE_AROUND")
			iBestCount=0
			pBestCity=0
			for icity in range(pPlayer.getNumCities()):
				pCity = pPlayer.getCity(icity)
				if not pCity.isNone():			
					iCount=0
					for iI in range(1, 21):
						pPlot2 = pCity.getCityIndexPlot(iI)					
						if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
							if pPlot2.getOwner()==pUnit.getOwner():
								if not (pPlot2.getImprovementType() != -1 and (gc.getImprovementInfo(pPlot2.getImprovementType()).isUnique() == true)):									
									if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_WATER1')):
										if smokeb:
											if (pPlot2.getImprovementType() == gc.getInfoTypeForString('IMPROVEMENT_SMOKE')):
												iCount=iCount+1
										if (desertb or pPlot.isRiver()):
											if (pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_DESERT') and not pPlot2.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')):
												if not pPlot2.getFeatureType() == gc.getInfoTypeForString('FEATURE_OASIS'):											
													iCount=iCount+1
									if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SUN1')):
										if snowb:
											if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_SNOW'):
												iCount=iCount+1								
										if tundrab:
											if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_TUNDRA'):
												iCount=iCount+1								
										if marshb:
											if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_MARSH'):
												iCount=iCount+1								
										if grassb:
											if pPlot2.getTerrainType()==gc.getInfoTypeForString('TERRAIN_GRASS'):
												iCount=iCount+1
									if hellterrb:								
										if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_LIFE1')):
											if (pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BROKEN_LANDS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BURNING_SANDS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SHALLOWS')):
												iCount=iCount+1
									if treesb:
										if (pPlot2.getFeatureType() == -1):
											if (pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_GRASS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_PLAINS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_TUNDRA')):										
												if not pPlot2.isCity():
													if (pPlot2.getImprovementType()==-1 or treesimpb):										
														iCount=iCount+1													
				
					if (iCount>iBestCount):
						pBestCity=pCity
						iBestCount=iCount
			if (pBestCity!=0):
				pCPlot = pBestCity.plot()
				CX = pCPlot.getX()
				CY = pCPlot.getY()	
				pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, CX, CY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)														
				return 1
			return 0
			
# Returns Promotiontype or -1 for no Promotion
	def AI_MagePromotion(self, argsList):
		pUnit = argsList[0]
		pPlot = pUnit.plot()
		pPlayer = gc.getPlayer(pUnit.getOwner())				
		eTeam = gc.getTeam(pPlayer.getTeam())		
		iPromotion = -1
		if pPlot.isCity():
			pCity=pPlot.getPlotCity()

#		if CyGame().getSorenRandNum(100, "Don't have check promotions every turn")	<70:
#			return -1
#OVERVIEW
#DIFFERENT FUNCTION FOR UNITAI_MAGE,UNITAI_TERRAFORMER, UNITAI_WARWIZARD
#
#1 List of available Promotion for the UNITAI
#2 Setting StackvaluesMod(Should several mages in the stack be able to cast the spell?)
#3 Adding CivValues
#4 Modify Spells by their action types (Mages with every turn Spells will prefere to add permanant spells)
#5 Add general Spellvalue for the UNITAI
#6 Make sure Adepts will take promos if they are needed for later promos
#7 Make sure Adepts will take promotions if they have enough XP to Upgrade to Mages

#------------
#UNITAI_MAGE
#------------			
		if (pUnit.getUnitAIType()==gc.getInfoTypeForString('UNITAI_MAGE')):
		
#Useless Spells should get a modifier of -10000
#Civvalues should be between 0 and 500
#And Spellvalues between 0 and 1000


#---------------------	
#List of available Promotions
#What Spells need a mage that buffs/defends cities?
#---------------------	
			sType = ['PROMOTION_BODY1','PROMOTION_BODY2','PROMOTION_CHAOS1','PROMOTION_CHAOS2']
			sType = sType +['PROMOTION_DEATH1','PROMOTION_DEATH2','PROMOTION_EARTH1','PROMOTION_ENTROPY1','PROMOTION_ENCHANTMENT1','PROMOTION_ENCHANTMENT2']
			sType = sType +['PROMOTION_MIND1','PROMOTION_MIND2','PROMOTION_NATURE1','PROMOTION_SHADOW1']
			sType = sType +['PROMOTION_SPIRIT1','PROMOTION_SPIRIT2']
			sType = sType +['PROMOTION_COMBAT1','PROMOTION_COMBAT2','PROMOTION_COMBAT3','PROMOTION_COMBAT4']

#---------------------				
#StackvaluesMod 
# 0 = doesn't matter, -100 = no way (other values are more interesting for offensive spellcasting
#---------------------	
			lStackvaluesMod = [-100,-100,0,-100,-100]
			lStackvaluesMod = lStackvaluesMod+[0,0,-100,0,-100,-100]
			lStackvaluesMod = lStackvaluesMod+[0,-100,0,-100,-100]
			lStackvaluesMod = lStackvaluesMod+[-100,-100]
			lStackvaluesMod = lStackvaluesMod+[0,0,0,0]
			
			lValues = [0]
			for i in range(len(sType)):
				lValues=lValues+[0]

#---------------------					
#Adding Civ Values
#---------------------	
#Amurites				
#Balseraph				
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS'):
				lValues[sType.index('PROMOTION_CHAOS1')]+=500
				lValues[sType.index('PROMOTION_CHAOS2')]+=500											
#Luchuirp				
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				lValues[sType.index('PROMOTION_ENCHANTMENT1')]+=500
				lStackvaluesMod[sType.index('PROMOTION_ENCHANTMENT1')]=-2				
#SHEAIM				
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				lValues[sType.index('PROMOTION_DEATH1')]+=2000			
				lValues[sType.index('PROMOTION_DEATH2')]+=2000							
				
				#---------------------	
#Modify Spells by their Stack Value (is it good to have several mages able to cast the spell?)
#---------------------							
			for i in range(len(sType)):
				lPromonbr=0
				for ii in range(pPlot.getNumUnits()):				
					if pPlot.getUnit(ii).isHasPromotion(gc.getInfoTypeForString(sType[i])):
						lPromonbr+=1
				lValues[i]+=lPromonbr*lStackvaluesMod[i]*100
#---------------------					
#Modify Spells by their action type (is it needed to cast them every turn?)
#---------------------				
			bcastoffspell=false
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1')):
				bcastoffspell=true				
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS1')):
				bcastoffspell=true				
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1')):
				bcastoffspell=true				
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND2')):
				bcastoffspell=true
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW1')):
				bcastoffspell=true
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				lValues[sType.index('PROMOTION_ENCHANTMENT1')]+=1000																	
				
			if not bcastoffspell:
				for i in range(len(sType)):
					lValues[sType.index('PROMOTION_DEATH1')]+=1000				
					lValues[sType.index('PROMOTION_CHAOS1')]+=1000				
					lValues[sType.index('PROMOTION_ENTROPY1')]+=1000				
					lValues[sType.index('PROMOTION_MIND2')]+=1000
					lValues[sType.index('PROMOTION_SHADOW1')]+=1000														

#---------------------					
#Spell Usefullness						
#Some are better than others...
#No, we don't use the XML file, cause these are only for city defenders
#But make sure Adepts take combat promos if necessary to upgrade to mages
#---------------------
			for i in range(len(sType)):
#Permanent Spells						
				if sType[i]=='PROMOTION_BODY2':								
					lValues[i]=lValues[i]+500									
				elif sType[i]=='PROMOTION_EARTH1':
					lValues[i]=lValues[i]+800
				elif sType[i]=='PROMOTION_MIND1':
					lValues[i]=lValues[i]+200
				elif sType[i]=='PROMOTION_SPIRIT2':
					if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):				
						lValues[i]=lValues[i]+300
				elif sType[i]=='PROMOTION_ENCHANTMENT1':						
					if pPlot.isCity():
						lValues[i]=lValues[i]+250
						if (pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TRAINING_YARD')) == 1):
							lValues[i]=lValues[i]+500
				elif sType[i]=='PROMOTION_ENCHANTMENT2':
					if pPlot.isCity():
						lValues[i]=lValues[i]+250
						if (pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_TRAINING_YARD')) == 1):
							lValues[i]=lValues[i]+500

#Powerfull debuffs
				elif sType[i]=='PROMOTION_DEATH1':
					lValues[i]=lValues[i]+100
				elif sType[i]=='PROMOTION_DEATH2':
					lValues[i]=lValues[i]+400				
				elif sType[i]=='PROMOTION_CHAOS1':
					lValues[i]=lValues[i]+150
				elif sType[i]=='PROMOTION_SHADOW1':
					lValues[i]=lValues[i]+130					
				elif sType[i]=='PROMOTION_ENTROPY1':
					lValues[i]=lValues[i]+800
				elif sType[i]=='PROMOTION_MIND2':
					lValues[i]=lValues[i]+500		
							
#Spells that are only needed for Upgrade
			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):			
				lValues[sType.index('PROMOTION_BODY1')]=lValues[sType.index('PROMOTION_BODY2')]+10									
				lValues[sType.index('PROMOTION_SPIRIT1')]=lValues[sType.index('PROMOTION_SPIRIT2')]+10																			

#---------------------
#Make sure Adepts take combat promos if necessary to be able to upgrade to mage
#---------------------

			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):
				if (pUnit.getExperience()>=10 and pUnit.getLevel()<4 and pUnit.getUnitClassType()==gc.getInfoTypeForString('UNITCLASS_ADEPT')):
					lValues[sType.index('PROMOTION_COMBAT1')]=10
					lValues[sType.index('PROMOTION_COMBAT2')]=10
					lValues[sType.index('PROMOTION_COMBAT3')]=10
					lValues[sType.index('PROMOTION_COMBAT4')]=10				

#---------------------
#Choose the best Spell
#---------------------					
			iBestSpell=-1
			iBestSpellValue=0
			for i in range(len(sType)):
				if lValues[i]>iBestSpellValue:
					if pUnit.canPromote(gc.getInfoTypeForString(sType[i]),-1):
						iBestSpellValue=lValues[i]
						iBestSpell=i
#			CyInterface().addImmediateMessage('IBestSpell is'+sType[iBestSpell], "AS2D_NEW_ERA")										
#			CyInterface().addImmediateMessage('IBestSpell is'+sType[iBestSpell], "AS2D_NEW_ERA")				
#			CyInterface().addImmediateMessage('IValue is'+str(lValues[iBestSpell]), "AS2D_NEW_ERA")				
#			CyInterface().addImmediateMessage('IValue is'+str(sType.index('PROMOTION_COMBAT1')), "AS2D_NEW_ERA")							
						
			if iBestSpell!=-1:
				iBestSpell=gc.getInfoTypeForString(sType[iBestSpell])
				
			
			return iBestSpell

#------------
#UNITAI_WARWIZARD
#------------			
					
		if (pUnit.getUnitAIType()==gc.getInfoTypeForString('UNITAI_WARWIZARD')):

			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):	
				countmages=0
				for ii in range (pPlot.getNumUnits()):
					if pPlot.getUnit(ii).getUnitCombatType()==gc.getInfoTypeForString('UNITCOMBAT_ADEPT'):
						countmages+=1
				if countmages<3:
					return -1
#Useless Spells should get a modifier of -10000
#Civvalues should be between 0 and 500
#And Spellvalues between 0 and 1000


#---------------------	
#List of available Promotions
#What Spells need a mage that buffs/defends cities?
#---------------------										

			sType = ['PROMOTION_AIR1','PROMOTION_AIR2','PROMOTION_BODY1','PROMOTION_BODY2','PROMOTION_CHAOS1']
			sType = sType +['PROMOTION_CHAOS2','PROMOTION_DEATH1','PROMOTION_DEATH2','PROMOTION_EARTH1','PROMOTION_EARTH2']
			sType = sType +['PROMOTION_ENTROPY1','PROMOTION_ENCHANTMENT1','PROMOTION_ENCHANTMENT2','PROMOTION_FIRE1','PROMOTION_FIRE2']
			sType = sType +['PROMOTION_LIFE1','PROMOTION_LIFE2','PROMOTION_MIND1']
			sType = sType +['PROMOTION_MIND2','PROMOTION_NATURE1','PROMOTION_NATURE2','PROMOTION_SHADOW1','PROMOTION_SHADOW2','PROMOTION_SPIRIT1']
			sType = sType +['PROMOTION_SUN1','PROMOTION_SUN2']
			sType = sType +['PROMOTION_COMBAT1','PROMOTION_COMBAT2','PROMOTION_COMBAT3','PROMOTION_COMBAT4','PROMOTION_MOBILITY1']
			
#---------------------				
#StackvaluesMod 
# 0 = doesn't matter, -100 = no way, normal values should be between 0 and -10 
#---------------------	
			lStackvaluesMod = [0,-2,-100,-100,-100] 
			lStackvaluesMod +=[-100,0,0,0,-2]
			lStackvaluesMod +=[-1,-100,-100,0,0]
			lStackvaluesMod +=[-100,-2,0,-7,0]			
			lStackvaluesMod +=[-2,-100,-100,-100,-100,-100]
			lStackvaluesMod +=[0,-2]
			lStackvaluesMod +=[0,0,0,0,0,]			

			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				lStackvaluesMod[sType.index('PROMOTION_ENCHANTMENT1')]=2			
			
			
			lValues = [0]
			for i in range(len(sType)):
				lValues=lValues+[0]

#---------------------					
#Adding Civ Values
#---------------------	
#Amurites				
#Balseraph				
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS'):
				lValues[sType.index('PROMOTION_CHAOS1')]+=500
				lValues[sType.index('PROMOTION_CHAOS2')]+=500
				
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_HIPPUS'):				
				lValues[sType.index('PROMOTION_MOBILITY1')]+=200													
#LJOSALFAR								
								
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):		
				lValues[sType.index('PROMOTION_FIRE2')]+=500
	
#Luchuirp				
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				lValues[sType.index('PROMOTION_ENCHANTMENT1')]+=500			
#SVARTALFAR				
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
				lValues[sType.index('PROMOTION_FIRE2')]+=500
#SHEIAM
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
				lValues[sType.index('PROMOTION_DEATH1')]+=500
				lValues[sType.index('PROMOTION_DEATH2')]+=500

#---------------------	
#Modify Spells by their Stack Value (is it good to have several mages able to cast the spell?)
#---------------------							
			for i in range(len(sType)):
				lPromonbr=0
				for ii in range(pPlot.getNumUnits()):				
					if pPlot.getUnit(ii).isHasPromotion(gc.getInfoTypeForString(sType[i])):
						lPromonbr+=1
				lValues[i]+=lPromonbr*lStackvaluesMod[i]*100
#---------------------					
#Modify Spells by their action type (is it needed to cast them every turn?)
#---------------------				
			bcastoffspell=false
			if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_AIR2')):
				bcastoffspell=true						
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_CHAOS1')):
				bcastoffspell=true								
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH1')):
				bcastoffspell=true				
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DEATH2')):
				bcastoffspell=true				
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_ENTROPY1')):
				bcastoffspell=true
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_FIRE2')):
				bcastoffspell=true								
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_MIND2')):
				bcastoffspell=true
			elif pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_SHADOW1')):
				bcastoffspell=true
				
			if not bcastoffspell:
				for i in range(len(sType)):
					lValues[sType.index('PROMOTION_AIR2')]+=1000
					lValues[sType.index('PROMOTION_CHAOS1')]+=1000
					lValues[sType.index('PROMOTION_DEATH1')]+=1000
					lValues[sType.index('PROMOTION_DEATH2')]+=1000
					lValues[sType.index('PROMOTION_ENTROPY1')]+=1000
					lValues[sType.index('PROMOTION_FIRE2')]+=1000								
					lValues[sType.index('PROMOTION_MIND2')]+=1000
					lValues[sType.index('PROMOTION_SHADOW1')]+=1000
					
			if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
				lValues[sType.index('PROMOTION_ENCHANTMENT1')]+=1000																	
					
#---------------------					
#Spell Usefullness						
#Some are better than others...
#No, we don't use the XML file, cause these are only for city defenders
#But make sure Adepts take combat promos if necessary to upgrade to mages
#---------------------

#Permanent Spells
			lValues[sType.index('PROMOTION_CHAOS1')]+=250														
			lValues[sType.index('PROMOTION_SHADOW1')]+=270
			lValues[sType.index('PROMOTION_SHADOW2')]+=270
			lValues[sType.index('PROMOTION_NATURE1')]+=280
			lValues[sType.index('PROMOTION_SPIRIT1')]+=300			
			lValues[sType.index('PROMOTION_ENCHANTMENT1')]+=300
			lValues[sType.index('PROMOTION_ENCHANTMENT2')]+=300
			lValues[sType.index('PROMOTION_NATURE2')]+=300
			lValues[sType.index('PROMOTION_BODY1')]+=500									
			lValues[sType.index('PROMOTION_BODY2')]+=500			
#Powerfull debuffs			
			lValues[sType.index('PROMOTION_EARTH2')]+=100
			lValues[sType.index('PROMOTION_MIND2')]+=400
			lValues[sType.index('PROMOTION_SUN2')]+=400
			lValues[sType.index('PROMOTION_ENTROPY1')]+=800																							
#Direct damage
			lValues[sType.index('PROMOTION_LIFE2')]+=0 #definetly needs some check																													
			lValues[sType.index('PROMOTION_FIRE2')]+=200																							
			lValues[sType.index('PROMOTION_AIR2')]+=500									

							
#Spells that are only needed for Upgrade			
			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):			
				lValues[sType.index('PROMOTION_EARTH1')]=lValues[sType.index('PROMOTION_EARTH2')]+10
				lValues[sType.index('PROMOTION_MIND1')]=lValues[sType.index('PROMOTION_MIND2')]+10
				lValues[sType.index('PROMOTION_LIFE1')]=lValues[sType.index('PROMOTION_LIFE2')]+10						
				lValues[sType.index('PROMOTION_FIRE1')]=lValues[sType.index('PROMOTION_FIRE2')]+10
				lValues[sType.index('PROMOTION_AIR1')]=lValues[sType.index('PROMOTION_AIR2')]+10

#---------------------
#Make sure Adepts take combat promos if necessary to be able to upgrade to mage
#---------------------

			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):
				if (pUnit.getExperience()>=10 and pUnit.getLevel()<4 and pUnit.getUnitClassType()==gc.getInfoTypeForString('UNITCLASS_ADEPT')):
					lValues[sType.index('PROMOTION_COMBAT1')]=10
					lValues[sType.index('PROMOTION_COMBAT2')]=10
					lValues[sType.index('PROMOTION_COMBAT3')]=10
					lValues[sType.index('PROMOTION_COMBAT4')]=10				
					lValues[sType.index('PROMOTION_MOBILITY1')]=10									
#---------------------
#Choose the best Spell
#---------------------					
			iBestSpell=-1
			iBestSpellValue=0
			for i in range(len(sType)):
				if lValues[i]>iBestSpellValue:
					if pUnit.canPromote(gc.getInfoTypeForString(sType[i]),-1):
						iBestSpellValue=lValues[i]
						iBestSpell=i
#			CyInterface().addImmediateMessage('IBestSpell is'+sType[iBestSpell], "AS2D_NEW_ERA")										
#			CyInterface().addImmediateMessage('IBestSpell is'+sType[iBestSpell], "AS2D_NEW_ERA")				
#			CyInterface().addImmediateMessage('IValue is'+str(lValues[iBestSpell]), "AS2D_NEW_ERA")				
#			CyInterface().addImmediateMessage('IValue is'+str(sType.index('PROMOTION_COMBAT1')), "AS2D_NEW_ERA")							
						
			if iBestSpell!=-1:
				iBestSpell=gc.getInfoTypeForString(sType[iBestSpell])
				
			
			return iBestSpell

#------------
#UNITAI_TERRAFORMER
#------------			
			
		if (pUnit.getUnitAIType()==gc.getInfoTypeForString('UNITAI_TERRAFORMER') or pUnit.getUnitAIType()==gc.getInfoTypeForString('UNITAI_MANA_UPGRADE')):
			if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):			
				if pUnit.canPromote(gc.getInfoTypeForString('PROMOTION_METAMAGIC1'),-1):
					return gc.getInfoTypeForString('PROMOTION_METAMAGIC1')					
				if pUnit.canPromote(gc.getInfoTypeForString('PROMOTION_METAMAGIC2'),-1):
					return gc.getInfoTypeForString('PROMOTION_METAMAGIC2')
				if (pUnit.getExperience()>10 and pUnit.getLevel()==4 and pUnit.getUnitClassType()==gc.getInfoTypeForString('UNITCLASS_ADEPT')):
					return -1
			if CyGame().getGlobalCounter()>15:
				if pUnit.canPromote(gc.getInfoTypeForString('PROMOTION_LIFE1'),-1):
					return gc.getInfoTypeForString('PROMOTION_LIFE1')
			if pUnit.canPromote(gc.getInfoTypeForString('PROMOTION_SUN1'),-1):
				return gc.getInfoTypeForString('PROMOTION_SUN1')
			if not pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL'):														
				if pUnit.canPromote(gc.getInfoTypeForString('PROMOTION_WATER1'),-1):
					return gc.getInfoTypeForString('PROMOTION_WATER1')
			if pUnit.canPromote(gc.getInfoTypeForString('PROMOTION_LIFE1'),-1):
				return gc.getInfoTypeForString('PROMOTION_LIFE1')
			if pUnit.canPromote(gc.getInfoTypeForString('PROMOTION_MOBILITY1'),-1):
					return gc.getInfoTypeForString('PROMOTION_MOBILITY1')
			if pUnit.canPromote(gc.getInfoTypeForString('PROMOTION_BODY1'),-1):
					return gc.getInfoTypeForString('PROMOTION_BODY1')
								

		return iPromotion

	def AI_Mage_UPGRADE_MANA(self, argsList):
		pUnit = argsList[0]

#-----------------------------------
#UNITAI_MANA_UPGRADE
#Terraformer looks around for mana, changes UNITAI if he doesn't found some
#
#
#Look for non raw mana and upgrade
#Look for raw mana, decide how to upgrade, and do it!
#Look for mana to dispel, and do it!
#-----------------------------------
		
		pPlot = pUnit.plot()
		pPlayer = gc.getPlayer(pUnit.getOwner())
		eTeam = gc.getTeam(pPlayer.getTeam())
		iX = pUnit.getX()
		iY = pUnit.getY()

		smokeb = true #Civ likes to put out smoke
		desertb = true #Civ likes to spring deserts
		snowb = true #Civ likes to scorch snow to tundra
		tundrab = true #Civ likes to scorch tundra to plains
		marshb = true #Civ likes to scorch marsh to grassland
		grassb = false #Civ likes to scorch grassland to plains			
		hellterrb = true #Civ likes to remove hell terrain

		if (pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL')):
			smokeb = false
#MALAKIM need SPRING to create floodplains sometimes
		if (pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_INFERNAL')): 
			desertb = false

		if (pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_ILLIANS')):
			snowb = false

		tundrab = false				
		marshb = false				
		
		if pPlayer.getCivilizationType()  == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
			hellterrb = false

#Look for non raw mana 		
		searchdistance=15
		imanatype = -1
		
		for isearch in range(1,searchdistance+1,1):
			if imanatype != -1: 
				break
			for iiY in range(iY-isearch, iY+isearch, 1):
				for iiX in range(iX-isearch, iX+isearch, 1):					
					pPlot2 = CyMap().plot(iiX,iiY)
					if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
						if pPlot2.getOwner() == pUnit.getOwner():
							if pPlot2.getBonusType(-1) != -1:
								iBonus = pPlot2.getBonusType(TeamTypes.NO_TEAM)
								if gc.getBonusInfo(iBonus).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_MANA'):
									if not pPlot2.isPlotGroupConnectedBonus(pUnit.getOwner(),iBonus):								
										imanatype=pPlot2.getBonusType(TeamTypes.NO_TEAM)
										if imanatype != -1:												
											for iBuild in range(gc.getNumBuildInfos()):
												if pUnit.canBuild(pPlot2,iBuild,false):
													pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
													pUnit.getGroup().pushMission(MissionTypes.MISSION_BUILD, iBuild, -1, 0, True, False, MissionAITypes.NO_MISSIONAI, pPlot, pUnit)
													return 1												

#Look for raw mana 		
		searchdistance=15
		imanatype = -1
		
		for isearch in range(1,searchdistance+1,1):
			if imanatype!=-1: 
				break
			for iiY in range(iY-isearch, iY+isearch, 1):
				for iiX in range(iX-isearch, iX+isearch, 1):
					pPlot2 = CyMap().plot(iiX,iiY)
					if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
						if pPlot2.getOwner() == pUnit.getOwner():
							if pPlot2.getBonusType(-1) != -1:
								iBonus = pPlot2.getBonusType(TeamTypes.NO_TEAM)
								if (iBonus == gc.getInfoTypeForString('BONUS_MANA') and not (iiX==iX and iiY==iY)):
									pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)																																												
									return 1
								elif iBonus == gc.getInfoTypeForString('BONUS_MANA'):
#---------------------
#Choose Mana to Build
#
#Set Flags
#
#----------------------	
#Set Flags
									deathmagicb=true
									holymagicb=true
									if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_EVIL'):
										holymagicb = false
									if pPlayer.getAlignment() == gc.getInfoTypeForString('ALIGNMENT_GOOD'):
										deathmagicb = false
#List of Useful Mana

									sType = ['BONUS_MANA_AIR','BONUS_MANA_BODY','BONUS_MANA_CHAOS','BONUS_MANA_DEATH']
									sType = sType +['BONUS_MANA_EARTH','BONUS_MANA_ENCHANTMENT','BONUS_MANA_ENTROPY','BONUS_MANA_FIRE']
									sType = sType +['BONUS_MANA_LAW','BONUS_MANA_LIFE','BONUS_MANA_MIND','BONUS_MANA_NATURE','BONUS_MANA_SHADOW']
									sType = sType +['BONUS_MANA_SPIRIT','BONUS_MANA_SUN','BONUS_MANA_WATER']

									sBuildType = ['BUILD_MANA_AIR','BUILD_MANA_BODY','BUILD_MANA_CHAOS','BUILD_MANA_DEATH']
									sBuildType = sBuildType +['BUILD_MANA_EARTH','BUILD_MANA_ENCHANTMENT','BUILD_MANA_ENTROPY','BUILD_MANA_FIRE']
									sBuildType = sBuildType +['BUILD_MANA_LAW','BUILD_MANA_LIFE','BUILD_MANA_MIND','BUILD_MANA_NATURE','BUILD_MANA_SHADOW']
									sBuildType = sBuildType +['BUILD_MANA_SPIRIT','BUILD_MANA_SUN','BUILD_MANA_WATER']
									
									lValues = [0]
									lStackvaluesMod = [-100] # by default a Civ doesn't like to stack mana
									for i in range(len(sType)):
										lValues=lValues+[0]
										lStackvaluesMod=lStackvaluesMod+[-100]
										
#---------------------					
#Adding Civ Values and their Mana stack values
#---------------------	
#Amurites				
#Balseraph				
									if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_BALSERAPHS'):
										lValues[sType.index('BONUS_MANA_CHAOS')]+=2000
#LJOSALFAR								
									if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LJOSALFAR'):		
										lValues[sType.index('BONUS_MANA_FIRE')]+=2000
										lStackvaluesMod[sType.index('BONUS_MANA_FIRE')]==-10
#Luchuirp				
									if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_LUCHUIRP'):
										lValues[sType.index('BONUS_MANA_ENCHANTMENT')]+=2000
										lValues[sType.index('BONUS_MANA_FIRE')]+=2000
										lStackvaluesMod[sType.index('BONUS_MANA_ENCHANTMENT')]==-20
#SVARTALFAR				
									if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SVARTALFAR'):
										lValues[sType.index('BONUS_MANA_FIRE')]+=2000
										lStackvaluesMod[sType.index('BONUS_MANA_FIRE')]==-10
#SHEIAM
									if pPlayer.getCivilizationType() == gc.getInfoTypeForString('CIVILIZATION_SHEAIM'):
										lValues[sType.index('BONUS_MANA_DEATH')]+=2000
										lValues[sType.index('BONUS_MANA_ENTROPY')]+=3000
										lStackvaluesMod[sType.index('BONUS_MANA_DEATH')]==0
									
#MANA TYPE VALUES									

#SPELL LEVEL 1
									
#Permanent
									lValues[sType.index('BONUS_MANA_NATURE')]+=50									
									lValues[sType.index('BONUS_MANA_MIND')]+=150
									lValues[sType.index('BONUS_MANA_SPIRIT')]+=200
									lValues[sType.index('BONUS_MANA_EARTH')]+=200
									lValues[sType.index('BONUS_MANA_BODY')]+=500
									lValues[sType.index('BONUS_MANA_ENCHANTMENT')]+=250
#per turn buffs
									lValues[sType.index('BONUS_MANA_CHAOS')]+=200
									lValues[sType.index('BONUS_MANA_SHADOW')]+=200
									lValues[sType.index('BONUS_MANA_ENTROPY')]+=700									
#Summons
									lValues[sType.index('BONUS_MANA_DEATH')]+=400

#SPELL LEVEL 2
									if pPlayer.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')):												
#Direct Damage
										lValues[sType.index('BONUS_MANA_AIR')]+=1000
										lValues[sType.index('BONUS_MANA_FIRE')]+=450
	#Permanent
										lValues[sType.index('BONUS_MANA_CHAOS')]+=0									
										lValues[sType.index('BONUS_MANA_SPIRIT')]+=100
										lValues[sType.index('BONUS_MANA_BODY')]+=100
	#per turn buffs
										lValues[sType.index('BONUS_MANA_EARTH')]+=100
										lValues[sType.index('BONUS_MANA_SHADOW')]+=100
										lValues[sType.index('BONUS_MANA_SUN')]+=400
										lValues[sType.index('BONUS_MANA_MIND')]+=400									
	#Summons									
										lValues[sType.index('BONUS_MANA_ENTROPY')]+=100
										lValues[sType.index('BONUS_MANA_DEATH')]+=200

#need mana for terraforming?						
									for pyCity in PyPlayer(pUnit.getOwner()).getCityList():
										pCity = pyCity.GetCy()
										pPlot3 = pCity.plot()
										cX = pPlot3.getX()
										cY = pPlot3.getY()										
										for iiX in range(cX-2, cX+2, 1):
											for iiY in range(cY-2, cY+2, 1):
												pPlot4 = CyMap().plot(iiX,iiY)
												if not (pPlot4.isNone() or pPlot4.isImpassable()):
													if pPlot4.getOwner()==pUnit.getOwner():
														if desertb:
															if (pPlot4.getTerrainType()==gc.getInfoTypeForString('TERRAIN_DESERT') and not pPlot4.getFeatureType() == gc.getInfoTypeForString('FEATURE_FLOOD_PLAINS')):
																lValues[sType.index('BONUS_MANA_WATER')]+=60
														if snowb:
															if pPlot4.getTerrainType()==gc.getInfoTypeForString('TERRAIN_SNOW'):
																lValues[sType.index('BONUS_MANA_SUN')]+=120
														if tundrab:														
															if pPlot4.getTerrainType()==gc.getInfoTypeForString('TERRAIN_TUNDRA'):
																lValues[sType.index('BONUS_MANA_SUN')]+=60
														if marshb:
															if pPlot4.getTerrainType()==gc.getInfoTypeForString('TERRAIN_MARSH'):
																lValues[sType.index('BONUS_MANA_SUN')]+=60
														if grassb:
															if pPlot4.getTerrainType()==gc.getInfoTypeForString('TERRAIN_GRASS'):
																lValues[sType.index('BONUS_MANA_SUN')]+=60
														if (hellterrb and CyGame().getGlobalCounter()>20):
															if (pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BROKEN_LANDS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_BURNING_SANDS') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_FIELDS_OF_PERDITION') or pPlot2.getTerrainType() == gc.getInfoTypeForString('TERRAIN_SHALLOWS')):
																lValues[sType.index('BONUS_MANA_LIFE')]+=100

#ManaStackvalues
									for i in range(len(sType)):
										iNumberMana=0
										iNumberMana+=pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString(sType[i]))													
										lValues[i]+=lStackvaluesMod[i]*100*iNumberMana
										
#Values for Victory Condition
									if (pPlayer.getArcaneTowerVictoryFlag()==1):
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_BODY'))==0:													
											lValues[sType.index('BONUS_MANA_BODY')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_LIFE'))==0:																								
											lValues[sType.index('BONUS_MANA_LIFE')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'))==0:																																			
											lValues[sType.index('BONUS_MANA_ENCHANTMENT')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_NATURE'))==0:																																		
											lValues[sType.index('BONUS_MANA_NATURE')]+=30000	

									if (pPlayer.getArcaneTowerVictoryFlag()==2):
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_LAW'))==0:													
											lValues[sType.index('BONUS_MANA_LAW')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_SUN'))==0:																								
											lValues[sType.index('BONUS_MANA_SUN')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_SPIRIT'))==0:																																			
											lValues[sType.index('BONUS_MANA_SPIRIT')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_MIND'))==0:																																		
											lValues[sType.index('BONUS_MANA_MIND')]+=30000	

									if (pPlayer.getArcaneTowerVictoryFlag()==3):
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_CHAOS'))==0:													
											lValues[sType.index('BONUS_MANA_CHAOS')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_DEATH'))==0:																								
											lValues[sType.index('BONUS_MANA_DEATH')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_ENTROPY'))==0:																																			
											lValues[sType.index('BONUS_MANA_ENTROPY')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_SHADOW'))==0:																																		
											lValues[sType.index('BONUS_MANA_SHADOW')]+=30000	
 
									if (pPlayer.getArcaneTowerVictoryFlag()==4):
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_EARTH'))==0:													
											lValues[sType.index('BONUS_MANA_EARTH')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_FIRE'))==0:																								
											lValues[sType.index('BONUS_MANA_FIRE')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_AIR'))==0:																																			
											lValues[sType.index('BONUS_MANA_AIR')]+=30000	
										if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_WATER'))==0:																																		
											lValues[sType.index('BONUS_MANA_WATER')]+=30000	
 
#									CyInterface().addImmediateMessage('TowerVictoryFlag is '+str(pPlayer.getArcaneTowerVictoryFlag()), "AS2D_NEW_ERA")										

#---------------------
#Choose the best MANA
#---------------------					
									iBestMana=-1
									iBestManaValue=0
									for i in range(len(sType)):
										if lValues[i]>iBestManaValue:
											if pUnit.canBuild(pPlot,gc.getInfoTypeForString(sBuildType[i]),false):
												iBestManaValue=lValues[i]
												iBestMana=i
												
									if iBestMana!=-1:
										pUnit.getGroup().pushMission(MissionTypes.MISSION_BUILD,gc.getInfoTypeForString(sBuildType[iBestMana]), -1, 0, False, False, MissionAITypes.MISSIONAI_BUILD, pPlot, pUnit)
										pPlot.setRouteType(gc.getInfoTypeForString('ROUTE_ROAD')) #help out the AI for the moment
										return 1
#Look for Mana to Dispel
		searchdistance=15
		   		
		if pUnit.isHasPromotion(gc.getInfoTypeForString('PROMOTION_METAMAGIC2')):		
			for isearch in range(1,searchdistance+1,1):				
				for iiY in range(iY-isearch, iY+isearch, 1):
					for iiX in range(iX-isearch, iX+isearch, 1):					
						pPlot2 = CyMap().plot(iiX,iiY)
						if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
							if pPlot2.getOwner()==pUnit.getOwner():
							
								if pPlot2.getBonusType(-1) != -1:
									iBonus = pPlot2.getBonusType(TeamTypes.NO_TEAM)
									if gc.getBonusInfo(iBonus).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_MANA'):
										bDispel = true

										if (pPlayer.getArcaneTowerVictoryFlag()==0):
											if CyGame().getSorenRandNum(50, "Don't have to Dispel all the Time"):									
												bDispel = false
										if (pPlayer.getArcaneTowerVictoryFlag()==1):
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_BODY'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_BODY'))==1:													
													bDispel = false
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_LIFE'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_LIFE'))==1:													
													bDispel = false									
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_ENCHANTMENT'))==1:													
													bDispel = false									
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_NATURE'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_NATURE'))==1:													
													bDispel = false																						

										if (pPlayer.getArcaneTowerVictoryFlag()==2):
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_LAW'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_LAW'))==1:													
													bDispel = false
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_SUN'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_SUN'))==1:													
													bDispel = false									
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_SPIRIT'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_SPIRIT'))==1:													
													bDispel = false									
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_MIND'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_MIND'))==1:													
													bDispel = false																															

										if (pPlayer.getArcaneTowerVictoryFlag()==3):
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_CHAOS'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_CHAOS'))==1:													
													bDispel = false
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_DEATH'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_DEATH'))==1:													
													bDispel = false									
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_ENTROPY'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_ENTROPY'))==1:													
													bDispel = false									
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_SHADOW'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_SHADOW'))==1:													
													bDispel = false	
														 
										if (pPlayer.getArcaneTowerVictoryFlag()==4):
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_EARTH'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_EARTH'))==1:													
													bDispel = false
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_FIRE'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_FIRE'))==1:													
													bDispel = false									
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_AIR'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_AIR'))==1:													
													bDispel = false									
											if iBonus == gc.getInfoTypeForString('BONUS_MANA_WATER'):
												if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_WATER'))==1:													
													bDispel = false	
																					
										if bDispel:
											if not (iiX==iX and iiY==iY):
#												CyInterface().addImmediateMessage('Searching for stuff to Dispel', "AS2D_NEW_ERA")																														
												pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, iiX, iiY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)																																			
												return 1
											if pUnit.canCast(gc.getInfoTypeForString('SPELL_DISPEL_MAGIC'),false):
												pUnit.cast(gc.getInfoTypeForString('SPELL_DISPEL_MAGIC'))
												return 1
#Dispel more if we seek Tower Victory Condition
			if (pPlayer.getArcaneTowerVictoryFlag()>0):												
				iBestCount=0
				pBestCity=0
				for icity in range(pPlayer.getNumCities()):
					pCity = pPlayer.getCity(icity)
					if not pCity.isNone():			
						iCount=0
						for iI in range(1, 21):
							pPlot2 = pCity.getCityIndexPlot(iI)					
							if not (pPlot2.isNone() or pPlot2.isImpassable() or pPlot2.isVisibleEnemyUnit(pUnit.getOwner())):
								if pPlot2.getOwner()==pUnit.getOwner():							
									if pPlot2.getBonusType(-1) != -1:
										iBonus = pPlot2.getBonusType(TeamTypes.NO_TEAM)
										if gc.getBonusInfo(iBonus).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_MANA'):					
											iCount=iCount+1
										if gc.getBonusInfo(iBonus).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_RAWMANA'):					
											iCount=iCount+1

						if (iCount>iBestCount):
							pBestCity=pCity
							iBestCount=iCount
				if (pBestCity!=0):
					pCPlot = pBestCity.plot()
					CX = pCPlot.getX()
					CY = pCPlot.getY()	
					pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, CX, CY, 0, False, False, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)														
					return 1
												
												
#found no mana, return 2 so UNITAI is set to UNITAI_TERRAFORMER
												
		return 2

#returns the current flag for Tower Victory
	def AI_TowerMastery(self, argsList):
		ePlayer = argsList[0]
		flag = argsList[1]

		pPlayer = gc.getPlayer(ePlayer)
		eTeam = gc.getTeam(pPlayer.getTeam())

#		CyInterface().addImmediateMessage('This is AI_TowerMastery ', "AS2D_NEW_ERA")												
#		CyInterface().addImmediateMessage('Flag is '+str(pPlayer.getArcaneTowerVictoryFlag()), "AS2D_NEW_ERA")										
		
		if flag==0:
			if eTeam.isHasTech(gc.getInfoTypeForString('TECH_SORCERY')) == False :
				return 0
			if pPlayer.getNumAvailableBonuses(gc.getInfoTypeForString('BONUS_MANA_METAMAGIC'))==0:				
				return 0

			possiblemana=0
			for i in range (CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if (pPlot.getOwner()==ePlayer):
					if pPlot.getBonusType(-1) != -1:
						iBonus = pPlot.getBonusType(TeamTypes.NO_TEAM)
						if gc.getBonusInfo(iBonus).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_MANA'):					
							possiblemana=possiblemana+1
						if gc.getBonusInfo(iBonus).getBonusClassType() == gc.getInfoTypeForString('BONUSCLASS_RAWMANA'):					
							possiblemana=possiblemana+1

			if possiblemana<4:
				return 0
			
			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_ALTERATION'))==0:
				return 1
				
			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_DIVINATION'))==0:
				return 2

			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'))==0:
				return 3

			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS'))==0:
				return 4
				
		if flag==1:
			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_ALTERATION'))>0:			
				return 0
			else:
				return 1
				
		if flag==2:
			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_DIVINATION'))>0:			
				return 0
			else:
				return 2

		if flag==3:
			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_NECROMANCY'))>0:			
				return 0
			else:
				return 3

		if flag==4:
			if pPlayer.getBuildingClassCount(gc.getInfoTypeForString('BUILDINGCLASS_TOWER_OF_THE_ELEMENTS'))>0:			
				return 0
			else:
				return 4
				
		return 0
