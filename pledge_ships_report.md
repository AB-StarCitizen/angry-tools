# Star Citizen Ownable (Pledge) Ships & Components Catalog

This report compiles a list of **player-pledgeable (ownable) ships, ground vehicles, and components** identified directly from the source game data files.

## 1. Methodology
We identified player-ownable assets by cross-referencing files in the following folders:
- **Showroom Displays**: `entities/scitem/shopdisplays/vehicle/*.json` - These files define showroom pedestals in showrooms (e.g. Astro Armada, New Deal). They map specific ship classes using `RequiredPortTags` to prevent AI-only variants from displaying.
- **Entitlements**: Base player ships contain `DefaultEntitlementEntityParams` in their static class data (pointing to account entitlements), while AI-only variants (e.g., `_pu_ai_crim`) do not.

## 2. Spaceships Catalog

Here is the list of player-ownable spaceships grouped by manufacturer:

### Aegis Dynamics (28 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Aegis Dynamics Avenger Stalker | `AEGS_Avenger_Stalker` | interceptor | combat |
| Aegis Dynamics Avenger Titan | `AEGS_Avenger_Titan` | lightfreight | transporter |
| Aegis Dynamics Avenger Titan Renegade | `AEGS_Avenger_Titan_Renegade` | lightfreight | transporter |
| Aegis Dynamics Avenger Warlock | `AEGS_Avenger_Warlock` | interdiction | combat |
| Aegis Dynamics Eclipse | `AEGS_Eclipse` | stealthbomber | combat |
| Aegis Dynamics Gladius | `AEGS_Gladius` | lightfighter | combat |
| Aegis Dynamics Gladius Valiant | `AEGS_Gladius_Valiant` | lightfighter | combat |
| Aegis Dynamics Hammerhead | `AEGS_Hammerhead` | @item ShipFocus HeavyGunship | combat |
| Aegis Dynamics Hammerhead Showdown | `AEGS_Hammerhead_Showdown` | @item ShipFocus HeavyGunship | combat |
| Aegis Dynamics Idris M | `AEGS_Idris_M` | frigate | combat |
| Aegis Dynamics Idris P | `AEGS_Idris_P` | frigate | combat |
| Aegis Dynamics Reclaimer | `AEGS_Reclaimer` | heavysalvage | resources |
| Aegis Dynamics Reclaimer Showdown | `AEGS_Reclaimer_Showdown` | heavysalvage | resources |
| Aegis Dynamics Redeemer | `AEGS_Redeemer` | gunship | combat |
| Aegis Dynamics Retaliator | `AEGS_Retaliator` | modular | combat |
| Aegis Dynamics Sabre | `AEGS_Sabre` | stealthfighter | combat |
| Aegis Dynamics Sabre Comet | `AEGS_Sabre_Comet` | stealthfighter | combat |
| Aegis Dynamics Sabre Firebird | `AEGS_Sabre_Firebird` | stealthfighter | combat |
| Aegis Dynamics Sabre Peregrine | `AEGS_Sabre_Peregrine` | racing | competition |
| Aegis Dynamics Sabre Raven | `AEGS_Sabre_Raven` | interdiction | combat |
| Aegis Dynamics Vanguard | `AEGS_Vanguard` | heavyfighter | combat |
| Aegis Dynamics Vanguard Harbinger | `AEGS_Vanguard_Harbinger` | heavyfighterbomber | combat |
| Aegis Dynamics Vanguard Hoplite | `AEGS_Vanguard_Hoplite` | dropship | combat |
| Aegis Dynamics Vanguard Sentinel | `AEGS_Vanguard_Sentinel` | heavyfighterbomber | combat |

### Anvil Aerospace (31 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Anvil Aerospace Arrow | `ANVL_Arrow` | lightfighter | combat |
| Anvil Aerospace Asgard | `ANVL_Asgard` | dropship | combat |
| Anvil Aerospace C8 Pisces | `ANVL_C8_Pisces` | pathfinder | exploration |
| Anvil Aerospace C8R Pisces Rescue | `ANVL_C8R_Pisces` | medical | support |
| Anvil Aerospace C8X Pisces Expedition | `ANVL_C8X_Pisces_Expedition` | pathfinder | exploration |
| Anvil Aerospace Carrack | `ANVL_Carrack` | expedition | exploration |
| Anvil Aerospace Carrack BIS2950 | `ANVL_Carrack_BIS2950` | expedition | exploration |
| Anvil Aerospace Gladiator | `ANVL_Gladiator` | bomber | combat |
| Anvil Aerospace Hawk | `ANVL_Hawk` | lightfighter | combat |
| Anvil Aerospace Hornet F7A | `ANVL_Hornet_F7A_Mk1` | mediumfighter | combat |
| Anvil Aerospace Hornet F7A Mk2 | `ANVL_Hornet_F7A_Mk2` | mediumfighter | combat |
| Anvil Aerospace Hornet F7C | `ANVL_Hornet_F7C` | mediumfighter | combat |
| Anvil Aerospace Hornet F7C Mk2 | `ANVL_Hornet_F7C_Mk2` | mediumfighter | combat |
| Anvil Aerospace Hornet F7C Wildfire | `ANVL_Hornet_F7C_Wildfire` | mediumfighter | combat |
| Anvil Aerospace Hornet F7CM | `ANVL_Hornet_F7CM` | mediumfighter | combat |
| Anvil Aerospace Hornet F7CM Heartseeker Mk2 | `ANVL_Hornet_F7CM_Mk2_Heartseeker` | mediumfighter | combat |
| Anvil Aerospace Hornet F7CM Mk2 | `ANVL_Hornet_F7CM_Mk2` | mediumfighter | combat |
| Anvil Aerospace Hornet F7CR | `ANVL_Hornet_F7CR` | pathfinder | exploration |
| Anvil Aerospace Hornet F7CR Mk2 | `ANVL_Hornet_F7CR_Mk2` | pathfinder | combat |
| Anvil Aerospace Hornet F7CS | `ANVL_Hornet_F7CS` | stealthfighter | combat |
| Anvil Aerospace Hornet F7CS Mk2 | `ANVL_Hornet_F7CS_Mk2` | stealthfighter | combat |
| Anvil Aerospace Hurricane | `ANVL_Hurricane` | heavyfighter | combat |
| Anvil Aerospace Lightning F8 | `ANVL_Lightning_F8` | heavyfighter | combat |
| Anvil Aerospace Lightning F8C | `ANVL_Lightning_F8C` | heavyfighter | combat |
| Anvil Aerospace Paladin | `ANVL_Paladin` | @item ShipFocus Gunship | @item ShipFocus Gunship |
| Anvil Aerospace Terrapin | `ANVL_Terrapin` | pathfinder | support |
| Anvil Aerospace Terrapin Medic | `ANVL_Terrapin_Medic` | medical | support |
| Anvil Aerospace Valkyrie | `ANVL_Valkyrie` | dropship | combat |
| Anvil Aerospace Valkyrie CitizenCon | `ANVL_Valkyrie_CitizenCon` | dropship | combat |

### Argo Astronautics (5 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Argo Astronautics MPUV Tractor | `ARGO_MPUV_1T` | lightfreight | transporter |
| Argo Astronautics MPUV Transport | `ARGO_MPUV_Transport` | passenger | transporter |
| Argo Astronautics Mole | `ARGO_MOLE` | mediummining | resources |
| Argo Astronautics RAFT | `ARGO_RAFT` | mediumfreight | transporter |
| Argo Astronautics SRV | `ARGO_SRV` | recovery | support |

### Banu (1 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Banu Defender | `BANU_Defender` | lightfighter | combat |

### Consolidated Outland (7 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Consolidated Outland HoverQuad | `CNOU_HoverQuad` | passenger | exploration |
| Consolidated Outland Mustang Alpha | `CNOU_Mustang_Alpha` | starterlightfreight | multirole |
| Consolidated Outland Mustang Beta | `CNOU_Mustang_Beta` | pathfinder | exploration |
| Consolidated Outland Mustang Delta | `CNOU_Mustang_Delta` | lightfighter | combat |
| Consolidated Outland Mustang Gamma | `CNOU_Mustang_Gamma` | racing | competition |
| Consolidated Outland Mustang Omega | `CNOU_Mustang_Omega` | racing | competition |
| Consolidated Outland Nomad | `CNOU_Nomad` | starterlightfreight | transporter |

### Crusader Industries (9 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Crusader Industries A1 Spirit | `CRUS_Spirit_A1` | bomber | combat |
| Crusader Industries C1 Spirit | `CRUS_Spirit_C1` | lightfreight | transporter |
| Crusader Industries Intrepid | `CRUS_Intrepid` | starterlightfreight | @item ShipFocus Starter |
| Crusader Industries Star Runner | `CRUS_Star_Runner` | mediumfreight | transporter |
| Crusader Industries Starfighter Inferno | `CRUS_Starfighter_Inferno` | heavyfighter | combat |
| Crusader Industries Starfighter Ion | `CRUS_Starfighter_Ion` | heavyfighter | combat |
| Crusader Industries Starlifter A2 | `CRUS_Starlifter_A2` | heavybomber | combat |
| Crusader Industries Starlifter M2 | `CRUS_Starlifter_M2` | mediumfreight | transporter |

### Drake Interplanetary (21 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Drake Interplanetary Buccaneer | `DRAK_Buccaneer` | lightfighter | combat |
| Drake Interplanetary Caterpillar | `DRAK_Caterpillar` | mediumfreight | transporter |
| Drake Interplanetary Caterpillar ShipShowdown | `DRAK_Caterpillar_ShipShowdown` | mediumfreight | transporter |
| Drake Interplanetary Clipper | `DRAK_Clipper` | generalist | exploration |
| Drake Interplanetary Corsair | `DRAK_Corsair` | expedition | exploration |
| Drake Interplanetary Cutlass Black | `DRAK_Cutlass_Black` | lightfreight mediumfighter | multirole |
| Drake Interplanetary Cutlass Black ShipShowdown | `DRAK_Cutlass_Black_ShipShowdown` | lightfreight mediumfighter | multirole |
| Drake Interplanetary Cutlass Blue | `DRAK_Cutlass_Blue` | interdiction | combat |
| Drake Interplanetary Cutlass Red | `DRAK_Cutlass_Red` | medical | support |
| Drake Interplanetary Cutlass Steel | `DRAK_Cutlass_Steel` | dropship | combat |
| Drake Interplanetary Cutter | `DRAK_Cutter` | starterpathfinder | exploration |
| Drake Interplanetary Cutter Rambler | `DRAK_Cutter_Rambler` | expedition | exploration |
| Drake Interplanetary Cutter Scout | `DRAK_Cutter_Scout` | pathfinder | exploration |
| Drake Interplanetary Dragonfly | `DRAK_Dragonfly` | racing | competition |
| Drake Interplanetary Dragonfly Pink | `DRAK_Dragonfly_Pink` | racing | competition |
| Drake Interplanetary Dragonfly Yellow | `DRAK_Dragonfly_Yellow` | racing | competition |
| Drake Interplanetary Golem | `DRAK_Golem` | startermining | resources |
| Drake Interplanetary Golem OX | `DRAK_Golem_OX` | lightfreight | resources |
| Drake Interplanetary Herald | `DRAK_Herald` | mediumdata | transporter |
| Drake Interplanetary Vulture | `DRAK_Vulture` | lightsalvage | resources |

### Esperia (7 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Esperia Blade | `VNCL_Blade` | lightfighter | combat |
| Esperia Glaive | `VNCL_Glaive` | mediumfighter | combat |
| Esperia Prowler | `ESPR_Prowler` | dropship | combat |
| Esperia Prowler Utility | `ESPR_Prowler_Utility` | lightfreight | transporter |
| Esperia Talon | `ESPR_Talon` | lightfighter | combat |
| Esperia Talon Shrike | `ESPR_Talon_Shrike` | lightfighter | combat |
| Vanduul Scythe | `VNCL_Scythe` | mediumfighter | combat |

### Gatac Manufacture (1 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Gatac Manufacture Syulen | `GAMA_Syulen` | starterpathfinder | multirole |

### Greycat Industrial (1 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| GLSN Shiv | `GLSN_Shiv` | heavyfighter | combat |

### Kruger Intergalactic (4 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Kruger Intergalactic L21 Wolf | `KRIG_L21_Wolf` | lightfighter | combat |
| Kruger Intergalactic L22 Alpha Wolf | `KRIG_L22_AlphaWolf` | lightfighter | combat |
| Kruger Intergalactic P52 Merlin | `KRIG_P52_Merlin` | snubfighter | combat |
| Kruger Intergalactic P72 Archimedes | `KRIG_P72_Archimedes` | racing | competition |

### MISC (15 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| MISC Fortune | `MISC_Fortune` | lightsalvage | resources |
| MISC Freelancer | `MISC_Freelancer` | lightfreight | transporter |
| MISC Freelancer DUR | `MISC_Freelancer_DUR` | expedition | exploration |
| MISC Freelancer MAX | `MISC_Freelancer_MAX` | mediumfreight | transporter |
| MISC Freelancer MIS | `MISC_Freelancer_MIS` | gunship | combat |
| MISC Hull A | `MISC_Hull_A` | lightfreight | transporter |
| MISC Hull C | `MISC_Hull_C` | heavyfreight | transporter |
| MISC Prospector | `MISC_Prospector` | lightmining | resources |
| MISC Reliant | `MISC_Reliant` | starterlightfreight | transporter |
| MISC Reliant Mako | `MISC_Reliant_Mako` | reporting | support |
| MISC Reliant Sen | `MISC_Reliant_Sen` | lightscience | resources |
| MISC Reliant Tana | `MISC_Reliant_Tana` | lightfighter | combat |
| MISC Starfarer | `MISC_Starfarer` | heavyrefuelling | support |
| MISC Starlancer Max | `MISC_Starlancer_Max` | mediumfreight | transporter |
| MISC Starlancer TAC | `MISC_Starlancer_TAC` | gunship | combat |

### MRAI_2025 (2 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Mirai Guardian | `MRAI_Guardian` | heavyfighter | combat |
| Mirai Guardian MX | `MRAI_Guardian_MX` | heavyfighter | combat |

### Mirai (7 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| MISC Fury | `MISC_Fury` | snubfighter | combat |
| MISC Fury LX | `MISC_Fury_LX` | racing | competition |
| MISC Razor | `MISC_Razor` | racing | competition |
| MISC Razor EX | `MISC_Razor_EX` | stealthfighter | combat |
| MISC Razor LX | `MISC_Razor_LX` | racing | competition |
| Mirai Pulse | `MRAI_Pulse` | pathfinder | combat |
| Mirai Pulse LX | `MRAI_Pulse_LX` | racing | combat |

### Origin Jumpworks (15 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Origin Jumpworks 100i | `ORIG_100i` | starterpathfinder | exploration |
| Origin Jumpworks 125a | `ORIG_125a` | lightfighter | combat |
| Origin Jumpworks 135c | `ORIG_135c` | lightfreight | transporter |
| Origin Jumpworks 300i | `ORIG_300i` | @item ShipFocus LuxuryTouring | exploration |
| Origin Jumpworks 315p | `ORIG_315p` | pathfinder | exploration |
| Origin Jumpworks 325a | `ORIG_325a` | interceptor | combat |
| Origin Jumpworks 350r | `ORIG_350r` | racing | competition |
| Origin Jumpworks 400i | `ORIG_400i` | expedition | exploration |
| Origin Jumpworks 600i Touring | `ORIG_600i_Touring` | @item ShipFocus LuxuryTouring | exploration |
| Origin Jumpworks 85X | `ORIG_85X` | @item ShipFocus Touring | exploration |
| Origin Jumpworks 890Jump | `ORIG_890Jump` | @item ShipFocus LuxuryTouring | exploration |
| Origin Jumpworks X1 | `ORIG_X1` | passenger | exploration |
| Origin Jumpworks X1 Force | `ORIG_X1_Force` | passenger | combat |
| Origin Jumpworks X1 Velocity | `ORIG_X1_Velocity` | @item ShipFocus Racing | competition |
| Origin Jumpworks m50 | `ORIG_m50` | racing | competition |

### RSI_2025 (3 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Roberts Space Industries Meteor | `RSI_Meteor` | mediumfighter | combat |
| Roberts Space Industries Perseus | `RSI_Perseus` | @item ShipFocus HeavyGunship | combat |
| Roberts Space Industries Salvation | `RSI_Salvation` | startersalvage | resources |

### Roberts Space Industries (12 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Roberts Space Industries Aurora Mk2 | `RSI_Aurora_Mk2` | starterlightfighter | multirole |
| Roberts Space Industries Constellation Andromeda | `RSI_Constellation_Andromeda` | mediumfreightgunshio | multirole |
| Roberts Space Industries Constellation Aquila | `RSI_Constellation_Aquila` | expedition | exploration |
| Roberts Space Industries Constellation Phoenix | `RSI_Constellation_Phoenix` | @item ShipFocus LuxuryTouring | exploration |
| Roberts Space Industries Constellation Phoenix Emerald | `RSI_Constellation_Phoenix_Emerald` | @item ShipFocus LuxuryTouring | exploration |
| Roberts Space Industries Constellation Taurus | `RSI_Constellation_Taurus` | mediumfreight | transporter |
| Roberts Space Industries Mantis | `RSI_Mantis` | interdiction | combat |
| Roberts Space Industries Polaris | `RSI_Polaris` | corvette | combat |
| Roberts Space Industries Scorpius | `RSI_Scorpius` | heavyfighter | combat |
| Roberts Space Industries Scorpius Antares | `RSI_Scorpius_Antares` | heavyfighter | combat |
| Roberts Space Industries Zeus CL | `RSI_Zeus_CL` | mediumfreight | transporter |
| Roberts Space Industries Zeus ES | `RSI_Zeus_ES` | expedition | exploration |

### Vanduul (1 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Esperia Stinger | `VNCL_Stinger` | heavyfighter | combat |

### XNAA (4 ships)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| XNAA SantokYai | `XNAA_SanTokYai` | mediumfighter | combat |
| Xi'an Nox | `XIAN_Nox` | racing | competition |
| Xi'an Nox Kue | `XIAN_Nox_Kue` | racing | competition |
| Xi'an Scout | `XIAN_Scout` | lightfighter | combat |

## 3. Ground Vehicles & Power Suits Catalog

Here is the list of player-ownable ground vehicles and mechs:

### Anvil Aerospace (3 vehicles)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Anvil Aerospace Ballista | `ANVL_Ballista` | antiair | combat |
| Anvil Aerospace Centurion | `ANVL_Centurion` | antiair | combat |
| Anvil Aerospace Spartan | `ANVL_Spartan` | passenger | combat |

### Argo Astronautics (2 vehicles)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Argo ATLS Power Suit | `argo_atls` | Loader / Exoskeleton | Industrial / Cargo |
| Argo Astronautics CSV Cargo | `ARGO_CSV_Cargo` | lightfreight | transporter |

### Drake Interplanetary (1 vehicles)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Drake Interplanetary Mule | `DRAK_Mule` | lightfreight | transporter |

### Greycat Industrial (6 vehicles)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Greycat Industrial MDC | `GRIN_MDC` | antiair | ground |
| Greycat Industrial MTC | `GRIN_MTC` | passenger | ground |
| Greycat Industrial PTV | `GRIN_PTV` | passenger | transporter |
| Greycat Industrial ROC | `GRIN_ROC` | lightmining | resources |
| Greycat Industrial ROC DS | `GRIN_ROC_DS` | lightmining | resources |
| Greycat Industrial STV | `GRIN_STV` | passenger | transporter |

### Roberts Space Industries (3 vehicles)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Roberts Space Industries Lynx | `RSI_Lynx` | @item ShipFocus LuxuryTouring | transporter |
| Roberts Space Industries URSA Medivac | `RSI_Ursa_Medivac` | medical | support |
| Roberts Space Industries Ursa Rover | `RSI_Ursa_Rover` | pathfinder | exploration |

### Tumbril Land Systems (9 vehicles)
| Name | Class Name | Role | Career |
| :--- | :--- | :--- | :--- |
| Tumbril Land Systems Cyclone | `TMBL_Cyclone` | passenger | combat |
| Tumbril Land Systems Cyclone AA | `TMBL_Cyclone_AA` | antiair | combat |
| Tumbril Land Systems Cyclone MT | `TMBL_Cyclone_MT` | antiair | combat |
| Tumbril Land Systems Cyclone RC | `TMBL_Cyclone_RC` | racing | competition |
| Tumbril Land Systems Cyclone RN | `TMBL_Cyclone_RN` | pathfinder | exploration |
| Tumbril Land Systems Cyclone TR | `TMBL_Cyclone_TR` | antivehicle | combat |
| Tumbril Land Systems Nova | `TMBL_Nova` | heavytank | combat |
| Tumbril Land Systems Storm | `TMBL_Storm` | lighttank | combat |
| Tumbril Land Systems Storm AA | `TMBL_Storm_AA` | lighttank | combat |

## 4. User-Ownable Ship Components

Standard ship components are player-ownable in-game (purchasable at shop terminals) if they have `SCItemPurchasableParams` in their definition JSON and do not belong to NPC-only/AI loadouts.

Here is the breakdown of ownable component types found in the database:

| Component Type | Database Count | Description |
| :--- | :---: | :--- |
| Paints | 1012 | General ship equipment or attachment. |
| ManneuverThruster | 817 | General ship equipment or attachment. |
| SeatAccess | 551 | General ship equipment or attachment. |
| WeaponAttachment | 491 | General ship equipment or attachment. |
| WeaponPersonal | 413 | General ship equipment or attachment. |
| Seat | 389 | General ship equipment or attachment. |
| MainThruster | 348 | General ship equipment or attachment. |
| Display | 316 | General ship equipment or attachment. |
| Turret | 277 | Manned and remote weapon/utility turrets. |
| FlightController | 212 | General ship equipment or attachment. |
| SeatDashboard | 199 | General ship equipment or attachment. |
| Armor | 199 | General ship equipment or attachment. |
| WeaponGun | 192 | Ship board weapons, including laser repeaters, ballistics, distortions, and cannons. |
| WeaponDefensive | 174 | General ship equipment or attachment. |
| FuelTank | 165 | General ship equipment or attachment. |
| Misc | 162 | General ship equipment or attachment. |
| DockingCollar | 156 | General ship equipment or attachment. |
| UNDEFINED | 150 | General ship equipment or attachment. |
| FuelIntake | 147 | General ship equipment or attachment. |
| QuantumFuelTank | 140 | General ship equipment or attachment. |
| MissileLauncher | 130 | Missile racks that hold ammunition packages. |
| ShieldController | 129 | General ship equipment or attachment. |
| CargoGrid | 124 | General ship equipment or attachment. |
| TurretBase | 121 | General ship equipment or attachment. |
| Cargo | 95 | General ship equipment or attachment. |
| PowerPlant | 83 | Power plants generating energy for ship systems and thrusters. |
| Cooler | 81 | Coolers managing thermodynamic heat accumulation. |
| Radar | 76 | General ship equipment or attachment. |
| Shield | 73 | Shield generators providing protection against damage. |
| Missile | 67 | Missiles and torpedoes loaded on ordnance racks. |
| QuantumDrive | 63 | Quantum drives for interstellar propulsion. |
| AttachedPart | 61 | General ship equipment or attachment. |
| Player | 49 | General ship equipment or attachment. |
| Usable | 41 | General ship equipment or attachment. |
| Room | 36 | General ship equipment or attachment. |
| Container | 32 | General ship equipment or attachment. |
| ExternalFuelTank | 31 | General ship equipment or attachment. |
| MiningModifier | 30 | Sub-items attached to mining lasers to tweak mining properties. |
| AIModule | 26 | General ship equipment or attachment. |
| Module | 24 | General ship equipment or attachment. |
| WeaponMining | 23 | General ship equipment or attachment. |
| Door | 21 | General ship equipment or attachment. |
| ToolArm | 16 | General ship equipment or attachment. |
| SalvageController | 16 | General ship equipment or attachment. |
| WheeledController | 14 | General ship equipment or attachment. |
| Relay | 13 | General ship equipment or attachment. |
| UtilityTurret | 12 | General ship equipment or attachment. |
| TractorBeam | 12 | General ship equipment or attachment. |
| Light | 12 | General ship equipment or attachment. |
| LifeSupportGenerator | 12 | General ship equipment or attachment. |
| JumpDrive | 12 | General ship equipment or attachment. |
| MissileController | 11 | General ship equipment or attachment. |
| Gadget | 10 | General ship equipment or attachment. |
| WeaponController | 9 | General ship equipment or attachment. |
| SalvageModifier | 9 | General ship equipment or attachment. |
| SalvageHead | 9 | General ship equipment or attachment. |
| SalvageFillerStation | 8 | General ship equipment or attachment. |
| GroundVehicleMissileLauncher | 8 | General ship equipment or attachment. |
| SelfDestruct | 7 | General ship equipment or attachment. |
| EMP | 7 | General ship equipment or attachment. |
| SalvageInternalStorage | 6 | General ship equipment or attachment. |
| QuantumInterdictionGenerator | 6 | General ship equipment or attachment. |
| LandingSystem | 6 | General ship equipment or attachment. |
| Battery | 6 | General ship equipment or attachment. |
| BombLauncher | 5 | General ship equipment or attachment. |
| MiningController | 4 | General ship equipment or attachment. |
| Grenade | 3 | General ship equipment or attachment. |
| GravityGenerator | 3 | General ship equipment or attachment. |
| DockingAnimator | 3 | General ship equipment or attachment. |
| Bomb | 3 | General ship equipment or attachment. |
| SpaceMine | 2 | General ship equipment or attachment. |
| Scanner | 2 | General ship equipment or attachment. |
| DoorController | 2 | General ship equipment or attachment. |
| AmmoBox | 2 | General ship equipment or attachment. |
| TowingBeam | 1 | General ship equipment or attachment. |
| TargetSelector | 1 | General ship equipment or attachment. |
| SalvageFieldSupporter | 1 | General ship equipment or attachment. |
| SalvageFieldEmitter | 1 | General ship equipment or attachment. |
| LightController | 1 | General ship equipment or attachment. |
| FuelController | 1 | General ship equipment or attachment. |
| EnergyController | 1 | General ship equipment or attachment. |
| CoolerController | 1 | General ship equipment or attachment. |
| CommsController | 1 | General ship equipment or attachment. |
| CapacitorAssignmentController | 1 | General ship equipment or attachment. |

*Report compiled successfully from game data records database.*