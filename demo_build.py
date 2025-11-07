"""
Demo build data for testing the application without a PoB code
"""
from datetime import datetime


def create_demo_build():
    """Create a demo Lightning Arrow Deadeye build"""
    build_id = 'demo_' + datetime.now().strftime('%Y%m%d%H%M%S')

    demo_build = {
        'id': build_id,
        'name': 'Lightning Arrow Deadeye (Demo Build)',
        'class': 'Ranger',
        'ascendancy': 'Deadeye',
        'level': 90,
        'created_at': datetime.now().isoformat(),
        'pob_code': 'DEMO_BUILD',
        'skills': [
            {
                'label': 'Lightning Arrow - Main DPS',
                'enabled': True,
                'slot': 'Weapon 1',
                'gems': [
                    {'name': 'Lightning Arrow', 'level': '21', 'quality': '20', 'enabled': True},
                    {'name': 'Mirage Archer Support', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Elemental Damage with Attacks Support', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Inspiration Support', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Trinity Support', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Awakened Added Lightning Damage Support', 'level': '5', 'quality': '0', 'enabled': True},
                ]
            },
            {
                'label': 'Barrage - Single Target',
                'enabled': True,
                'slot': 'Weapon Swap',
                'gems': [
                    {'name': 'Barrage', 'level': '21', 'quality': '20', 'enabled': True},
                    {'name': 'Elemental Damage with Attacks Support', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Inspiration Support', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Trinity Support', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Awakened Added Lightning Damage Support', 'level': '5', 'quality': '0', 'enabled': True},
                ]
            },
            {
                'label': 'Auras',
                'enabled': True,
                'slot': 'Body Armour',
                'gems': [
                    {'name': 'Grace', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Determination', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Defiance Banner', 'level': '20', 'quality': '20', 'enabled': True},
                ]
            },
            {
                'label': 'Movement & Utility',
                'enabled': True,
                'slot': 'Boots',
                'gems': [
                    {'name': 'Blink Arrow', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Sniper\'s Mark', 'level': '20', 'quality': '20', 'enabled': True},
                    {'name': 'Mark On Hit Support', 'level': '20', 'quality': '0', 'enabled': True},
                ]
            },
            {
                'label': 'Defensive Setup',
                'enabled': True,
                'slot': 'Gloves',
                'gems': [
                    {'name': 'Cast when Damage Taken Support', 'level': '1', 'quality': '0', 'enabled': True},
                    {'name': 'Molten Shell', 'level': '10', 'quality': '20', 'enabled': True},
                    {'name': 'Immortal Call', 'level': '3', 'quality': '0', 'enabled': True},
                ]
            }
        ],
        'items': [
            {'slot': 'Weapon 1', 'name': 'Rare Thicket Bow\nAdds # to # Lightning Damage\n+# to Accuracy Rating\n+#% Critical Strike Chance\n+#% Attack Speed'},
            {'slot': 'Quiver', 'name': 'Hyrri\'s Demise\nFrenzy Charge on Kill\nAdds Cold Damage\n+# Life\n+#% Critical Strike Multiplier'},
            {'slot': 'Body Armour', 'name': 'Rare Evasion Chest\n+# to Maximum Life\n+#% to Elemental Resistances\n+# to Evasion Rating\nSuppression'},
            {'slot': 'Helmet', 'name': 'Rare Evasion Helmet\n+# to Maximum Life\n+#% to Elemental Resistances\n+# to Evasion Rating\nSuppression'},
            {'slot': 'Gloves', 'name': 'Rare Evasion Gloves\n+# to Maximum Life\n+#% to Elemental Resistances\nSuppression\nAccuracy Rating'},
            {'slot': 'Boots', 'name': 'Rare Evasion Boots\n+# to Maximum Life\n+#% to Elemental Resistances\n30% Movement Speed\nSuppression'},
            {'slot': 'Amulet', 'name': 'Rare Amulet\n+# to Maximum Life\n+#% to Elemental Resistances\nAdds Lightning Damage\n+# to Attributes'},
            {'slot': 'Ring 1', 'name': 'Rare Ring\n+# to Maximum Life\n+#% to Elemental Resistances\nAdds Lightning Damage\n+# to Accuracy'},
            {'slot': 'Ring 2', 'name': 'Rare Ring\n+# to Maximum Life\n+#% to Elemental Resistances\nAdds Lightning Damage\n+# to Accuracy'},
            {'slot': 'Belt', 'name': 'Rare Stygian Vise\n+# to Maximum Life\n+#% to Elemental Resistances\nIncreased Flask Charges Gained\n+#% Elemental Damage'},
        ],
        'tree': {
            'nodes': '1,2,3,4,5,6,7,8,9,10',  # Simplified for demo
            'url': 'Demo build - Import into Path of Building to see full tree',
            'sockets': '',
        },
        'notes': '''Lightning Arrow Deadeye - League Starter Build

OVERVIEW:
This is a fast-mapping Lightning Arrow build using the Deadeye ascendancy. Great for clearing maps quickly and scales well into endgame with investment.

PROS:
+ Excellent clear speed with chain
+ Good single target with Barrage swap
+ Zoom zoom fast mapping
+ Budget friendly league starter
+ Tanky with Determination + Grace

CONS:
- Can be squishy without proper gear
- Requires accuracy stacking
- Mana management early on
- Single target requires gem swap

LEVELING:
1-12: Use any bow skill (Caustic Arrow, Burning Arrow)
12-28: Switch to Lightning Arrow when available
28+: Add support gems as you progress
Maps: Full setup with auras

IMPORTANT GEAR:
- High DPS bow (Thicket or Imperial base)
- Life + Resistances on all rare gear
- Spell Suppression (aim for 100%)
- Accuracy rating (aim for 100% hit chance)
- Movement speed boots

PANTHEON:
Major: Soul of Lunaris (mapping) or Solaris (bossing)
Minor: Soul of Shakari (poison immunity)

BANDIT:
Kill All for +2 passive points

FLASKS:
- Life Flask with Bleed immunity
- Quicksilver Flask
- Diamond Flask (crit chance)
- Granite or Jade Flask (defense)
- Experimenter's Quartz Flask (phasing)

ENDGAME:
Focus on getting +1 arrows on quiver or bow, upgrading to Awakened gems, and stacking more crit multi and attack speed.
''',
        'milestones': [
            {'level': 1, 'act': 1, 'title': 'Start - Kill Hillock', 'description': 'Begin your journey'},
            {'level': 12, 'act': 1, 'title': 'Complete Act 1', 'description': 'Defeat Merveil'},
            {'level': 20, 'act': 2, 'title': 'Complete Act 2', 'description': 'Defeat Vaal Oversoul'},
            {'level': 28, 'act': 3, 'title': 'Complete Act 3', 'description': 'Defeat Dominus'},
            {'level': 35, 'act': 4, 'title': 'Complete Act 4', 'description': 'Defeat Malachai'},
            {'level': 40, 'act': 5, 'title': 'Complete Act 5 - First Kitava Fight', 'description': 'Defeat Kitava and receive -30% to all resistances'},
            {'level': 46, 'act': 6, 'title': 'Complete Act 6', 'description': 'Defeat Tsoagoth. Lilly Roth now sells ALL gems!'},
            {'level': 52, 'act': 7, 'title': 'Complete Act 7', 'description': 'Defeat Arakaali'},
            {'level': 58, 'act': 8, 'title': 'Complete Act 8', 'description': 'Defeat Lunaris & Solaris'},
            {'level': 62, 'act': 9, 'title': 'Complete Act 9', 'description': 'Defeat The Depraved Trinity. Blood Aqueduct is great for farming!'},
            {'level': 68, 'act': 10, 'title': 'Complete Act 10 - Final Story Boss', 'description': 'Defeat Kitava again. Another -30% to all resistances (total -60%)! Maps unlocked!'},
            {'level': 70, 'act': 11, 'title': 'White Maps (Tier 1-5)', 'description': 'Begin mapping. Focus on Atlas completion and capping resistances at 75%'},
            {'level': 73, 'act': 11, 'title': 'Yellow Maps (Tier 6-10)', 'description': 'Progress through yellow maps. Watch out for dangerous map mods'},
            {'level': 78, 'act': 11, 'title': 'Red Maps (Tier 11-16)', 'description': 'Tackle red maps. Ensure your defenses are solid'},
            {'level': 85, 'act': 11, 'title': 'Conquerors & Maven Content', 'description': 'Start engaging with endgame boss content and Maven invitations'},
            {'level': 90, 'act': 11, 'title': 'Pinnacle Content', 'description': 'Farm T16 maps and attempt pinnacle bosses (Maven, Exarch, Eater of Worlds, Uber Elder)'},
        ]
    }

    return demo_build, build_id


def get_demo_progress(build_id):
    """Get initial progress for demo build"""
    return {
        'current_level': 1,
        'current_act': 1,
        'completed_milestones': [],
        'completed_quests': [],
        'completed_labs': [],
        'completed_trials': [],
        'bandit_choice': 'kill_all'
    }
