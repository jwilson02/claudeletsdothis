"""
Quest rewards and important game progression data for Path of Exile
"""

# Important quest rewards by act
QUEST_REWARDS = {
    'act1': [
        {
            'quest': 'Enemy at the Gate',
            'rewards': ['Various support gems'],
            'location': 'Town - Nessa',
            'important': True,
            'notes': 'First support gem quest - choose based on your main skill'
        },
        {
            'quest': 'The Caged Brute',
            'rewards': ['Passive skill point'],
            'location': 'Town - Nessa',
            'important': True,
            'notes': 'First passive skill point quest'
        },
        {
            'quest': 'Breaking Some Eggs',
            'rewards': ['Various skill gems'],
            'location': 'Town - Nessa',
            'important': False,
            'notes': 'Additional skill gems'
        },
        {
            'quest': 'The Siren\'s Cadence',
            'rewards': ['Passive skill point', 'All Act 1 gems available'],
            'location': 'Town - Nessa',
            'important': True,
            'notes': 'Unlock all Act 1 gems for purchase'
        }
    ],
    'act2': [
        {
            'quest': 'Through Sacred Ground',
            'rewards': ['Passive skill point'],
            'location': 'Town - Helena',
            'important': True,
            'notes': 'Deal with the Bandit Lords first'
        },
        {
            'quest': 'Deal with the Bandits',
            'rewards': ['Passive skill point OR bandit reward'],
            'location': 'Forest areas',
            'important': True,
            'notes': 'Choose: Kill All (+2 passive points) or help Alira (mana regen, crit, resists) - Oak and Kraityn less common'
        },
        {
            'quest': 'Intruders in Black',
            'rewards': ['Passive skill point', 'All Act 2 gems available'],
            'location': 'Town - Helena',
            'important': True,
            'notes': 'Unlock all Act 2 gems for purchase'
        }
    ],
    'act3': [
        {
            'quest': 'Victario\'s Secrets',
            'rewards': ['Passive skill point'],
            'location': 'Town - Siosa',
            'important': True,
            'notes': 'Library quest - also unlocks Siosa as gem vendor'
        },
        {
            'quest': 'Sever the Right Hand',
            'rewards': ['Passive skill point', 'All Act 3 gems available'],
            'location': 'Town - Clarissa',
            'important': True,
            'notes': 'Unlock all Act 3 gems for purchase'
        },
        {
            'quest': 'Piety\'s Pets',
            'rewards': ['Skill point'],
            'location': 'Town - Clarissa',
            'important': True,
            'notes': 'After defeating Piety in Lunaris Temple'
        }
    ],
    'act4': [
        {
            'quest': 'An Indomitable Spirit',
            'rewards': ['Passive skill point'],
            'location': 'Town - Oyun',
            'important': True,
            'notes': 'Free Deshret\'s spirit'
        },
        {
            'quest': 'The Eternal Nightmare',
            'rewards': ['Passive skill point', 'All Act 4 gems available'],
            'location': 'Town - Tasuni',
            'important': True,
            'notes': 'Defeat Malachai'
        }
    ],
    'act5': [
        {
            'quest': 'The Key to Freedom',
            'rewards': ['Passive skill point'],
            'location': 'Town - Lani',
            'important': True,
            'notes': 'Free from Oriath Square'
        },
        {
            'quest': 'Death to Puritanism',
            'rewards': ['Passive skill point'],
            'location': 'Town - Vilenta',
            'important': True,
            'notes': 'Defeat High Templar Avarius'
        },
        {
            'quest': 'The Fall of Oriath',
            'rewards': ['Lose all resistances (-30%)', 'All prior gems available'],
            'location': 'Town',
            'important': True,
            'notes': 'After defeating Kitava - MASSIVE resistance penalty!'
        }
    ],
    'act6': [
        {
            'quest': 'The Cloven One',
            'rewards': ['Passive skill point'],
            'location': 'Town - Bestel',
            'important': True,
            'notes': 'Defeat Abberath'
        },
        {
            'quest': 'The Puppet Mistress',
            'rewards': ['Passive skill point'],
            'location': 'Town - Lilly Roth',
            'important': True,
            'notes': 'ALL gems now available from Lilly Roth!'
        }
    ],
    'act7': [
        {
            'quest': 'The Master of a Million Faces',
            'rewards': ['Passive skill point'],
            'location': 'Town - Helena',
            'important': True,
            'notes': 'Defeat Gruthkul'
        },
        {
            'quest': 'Queen of Despair',
            'rewards': ['Passive skill point'],
            'location': 'Town - Silk',
            'important': True,
            'notes': 'Defeat Arakaali'
        }
    ],
    'act8': [
        {
            'quest': 'Reflection of Terror',
            'rewards': ['Passive skill point'],
            'location': 'Town - Clarissa',
            'important': True,
            'notes': 'Defeat Yugul in Sewer area'
        },
        {
            'quest': 'The Gemling Legion',
            'rewards': ['Passive skill point'],
            'location': 'Town - Maramoa',
            'important': True,
            'notes': 'Clear Grain Gate'
        },
        {
            'quest': 'Love is Dead',
            'rewards': ['Passive skill point'],
            'location': 'Town - Clarissa',
            'important': True,
            'notes': 'Defeat Lunaris and Solaris'
        }
    ],
    'act9': [
        {
            'quest': 'Storm Blade',
            'rewards': ['Passive skill point'],
            'location': 'Town - Petarus & Vanja',
            'important': True,
            'notes': 'Deliver Storm Blade to Sin'
        },
        {
            'quest': 'Queen of the Sands',
            'rewards': ['Passive skill point'],
            'location': 'Town - Irasha',
            'important': True,
            'notes': 'Defeat Shakari in Desert'
        },
        {
            'quest': 'The Ruler of Highgate',
            'rewards': ['Passive skill point'],
            'location': 'Town - Sin',
            'important': True,
            'notes': 'Defeat the Depraved Trinity'
        }
    ],
    'act10': [
        {
            'quest': 'Vilenta\'s Vengeance',
            'rewards': ['Passive skill point'],
            'location': 'Town - Vilenta',
            'important': True,
            'notes': 'Complete Kitava\'s Horns quest'
        },
        {
            'quest': 'An End to Hunger',
            'rewards': ['Lose all resistances again (-30%, total -60%)', 'Access to maps'],
            'location': 'Town',
            'important': True,
            'notes': 'Defeat Kitava again - Another MASSIVE resistance penalty! You now need +135% to each resist to cap!'
        }
    ]
}

# Labyrinth trials tracking
LABYRINTH_TRIALS = {
    'normal': {
        'name': 'The Lord\'s Labyrinth (Normal)',
        'level': 33,
        'trials': [
            {'location': 'The Lower Prison', 'act': 1},
            {'location': 'The Chamber of Sins Level 2', 'act': 2},
            {'location': 'The Crypt Level 1', 'act': 2},
            {'location': 'The Chamber of Sins Level 2 (2nd trial)', 'act': 2},
            {'location': 'The Crematorium', 'act': 3},
            {'location': 'The Catacombs', 'act': 3}
        ],
        'reward': 'First Ascendancy (2 points)',
        'notes': 'Grants your first 2 Ascendancy points'
    },
    'cruel': {
        'name': 'The Lord\'s Labyrinth (Cruel)',
        'level': 55,
        'trials': [
            {'location': 'The Prison', 'act': 6},
            {'location': 'The Crypt', 'act': 7},
            {'location': 'The Chamber of Sins Level 2', 'act': 7}
        ],
        'reward': 'Second Ascendancy (4 total points)',
        'notes': 'Grants 2 more Ascendancy points (4 total)'
    },
    'merciless': {
        'name': 'The Lord\'s Labyrinth (Merciless)',
        'level': 68,
        'trials': [
            {'location': 'The Bath House', 'act': 8},
            {'location': 'The Tunnel', 'act': 9},
            {'location': 'The Ossuary', 'act': 10}
        ],
        'reward': 'Third Ascendancy (6 total points)',
        'notes': 'Grants 2 more Ascendancy points (6 total)'
    },
    'eternal': {
        'name': 'The Lord\'s Labyrinth (Eternal)',
        'level': 75,
        'trials': 'Complete trials in maps',
        'reward': 'Fourth Ascendancy (8 total points)',
        'notes': 'Find and complete 6 trials in maps, then run Eternal Lab for final 2 points (8 total)'
    }
}

# Important leveling tips by act
ACT_TIPS = {
    'act1': {
        'title': 'Act 1: The Twilight Strand',
        'tips': [
            'Pick up all Quicksilver flasks',
            'Don\'t worry about gear quality early - just keep moving',
            'Grab waypoints in every zone',
            'Use Rog in town for gear upgrades if playing current league',
            'Movement speed on boots is very valuable'
        ]
    },
    'act2': {
        'title': 'Act 2: The Wetlands',
        'tips': [
            'Decide on Bandit quest: Kill All for +2 passives (most common) or Help Alira for resists/crit/mana',
            'Start paying attention to elemental resistances',
            'Get a Quicksilver flask if you haven\'t already',
            'The Weaver\'s Chambers has good XP - can farm if underleveled'
        ]
    },
    'act3': {
        'title': 'Act 3: The City of Sarn',
        'tips': [
            'Visit Library early for quest and to unlock Siosa (sells ALL gems)',
            'Sarn is a huge city - grab all waypoints',
            'Start capping resistances (75% is cap)',
            'Consider getting better flasks - Staunching (bleed immune) is important',
            'Dominus fight has two phases - take your time'
        ]
    },
    'act4': {
        'title': 'Act 4: The Aqueduct',
        'tips': [
            'Aqueduct is great for farming Humility cards (Tabula Rasa)',
            'This act is shorter than others',
            'Malachai fight is challenging - be ready with capped resists and good flasks',
            'Get Granite or Basalt flask for physical damage reduction',
            'Kaom and Daresso must both be defeated before Harvest'
        ]
    },
    'act5': {
        'title': 'Act 5: The Slave Pens',
        'tips': [
            'After Kitava, you lose 30% to ALL resistances!',
            'Farm Act 4 Aqueduct if you need better gear before proceeding',
            'Life and resistances become crucial',
            'Start planning for the -30% resist penalty',
            'Innocence and Kitava are tough fights - be prepared'
        ]
    },
    'act6': {
        'title': 'Act 6: The Twilight Strand',
        'tips': [
            'After defeating Tsoagoth, Lilly Roth sells ALL gems!',
            'This is a good time to reorganize your gem setup',
            'Resistances are critical now after Act 5 penalty',
            'Consider farming Blood Aqueduct (Act 9) if gear is lacking',
            'Brine King quest unlocks useful Pantheon power'
        ]
    },
    'act7': {
        'title': 'Act 7: The Broken Bridge',
        'tips': [
            'This act has a lot of backtracking',
            'Grab the waypoint in Ashen Fields early',
            'Greust in town can help with Firefly quest',
            'Consider upgrading flasks to tier-appropriate levels',
            'Arakaali\'s Pantheon is very useful for many builds'
        ]
    },
    'act8': {
        'title': 'Act 8: The Toxic Conduits',
        'tips': [
            'This is a long act with lots of ground to cover',
            'Lunaris and Solaris bosses are separate - you fight both',
            'Good time to buy better gear if needed',
            'Start thinking about your final gem links',
            'Yugul Pantheon is great for reflect protection'
        ]
    },
    'act9': {
        'title': 'Act 9: The Foothills',
        'tips': [
            'Blood Aqueduct is THE farming zone - great layout and density',
            'Farm here for Humility cards, XP, or currency if needed',
            'Shakari Pantheon is excellent for poison immunity',
            'You\'re getting close to maps - ensure resistances are sorted',
            'Trinity fight can be tough - kite and dodge attacks'
        ]
    },
    'act10': {
        'title': 'Act 10: The Cathedral Rooftop',
        'tips': [
            'Final act! After Kitava you get ANOTHER -30% resist penalty (total -60%)',
            'You need +135% to each resistance to be capped!',
            'Farm Act 9 Blood Aqueduct if you need better gear',
            'After defeating Kitava, you unlock Maps!',
            'Consider running Normal/Cruel/Merciless lab before maps if you haven\'t',
            'Welcome to the endgame!'
        ]
    }
}

# Endgame progression milestones
ENDGAME_MILESTONES = [
    {
        'level': 68,
        'title': 'White Maps (Tier 1-5)',
        'description': 'Begin mapping - focus on completing the Atlas',
        'tips': 'Run every map once for completion bonus. Prioritize capping resistances at 75%.'
    },
    {
        'level': 70,
        'title': 'Complete Cruel Labyrinth',
        'description': 'Get your 3rd and 4th Ascendancy points if not done already',
        'tips': 'Should be easy at this level'
    },
    {
        'level': 73,
        'title': 'Yellow Maps (Tier 6-10)',
        'description': 'Progress through yellow maps',
        'tips': 'Watch out for dangerous map mods. Chaos resistance becomes more important.'
    },
    {
        'level': 75,
        'title': 'Complete Merciless Labyrinth',
        'description': 'Get your 5th and 6th Ascendancy points',
        'tips': 'This one can be challenging - make sure you have good gear'
    },
    {
        'level': 78,
        'title': 'Red Maps (Tier 11-16)',
        'description': 'Progress through red maps',
        'tips': 'Monsters are much stronger. Consider your build defenses carefully.'
    },
    {
        'level': 80,
        'title': 'Start Running Eternal Lab Trials',
        'description': 'Find 6 trials in maps to unlock Eternal Labyrinth',
        'tips': 'You can buy trial completions from other players using /global 820'
    },
    {
        'level': 82,
        'title': 'Complete Eternal Labyrinth',
        'description': 'Get your final Ascendancy points (7th and 8th)',
        'tips': 'Your character is now fully ascended! This is a major power spike.'
    },
    {
        'level': 85,
        'title': 'Conquerors & Maven',
        'description': 'Start engaging with endgame boss content',
        'tips': 'Focus on completing Atlas objectives and Maven invitations'
    },
    {
        'level': 90,
        'title': 'T16 Maps & Endgame Bosses',
        'description': 'Farm highest tier content and attempt pinnacle bosses',
        'tips': 'Consider The Maven, Searing Exarch, Eater of Worlds, and Uber Elder'
    }
]

def get_quest_rewards_for_act(act_num):
    """Get quest rewards for a specific act"""
    act_key = f'act{act_num}'
    return QUEST_REWARDS.get(act_key, [])

def get_act_tips(act_num):
    """Get tips for a specific act"""
    act_key = f'act{act_num}'
    return ACT_TIPS.get(act_key, {})
