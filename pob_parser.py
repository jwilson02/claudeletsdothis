"""
Path of Building (PoB) Code Parser
Handles importing and parsing PoB build codes
"""
import base64
import zlib
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any


class PoBParser:
    """Parse Path of Building export codes"""

    def __init__(self):
        self.build_data = {}

    def decode_pob_code(self, pob_code: str) -> str:
        """Decode a PoB code to XML string"""
        try:
            # Remove any whitespace
            pob_code = pob_code.strip().replace('\n', '').replace('\r', '')

            # Decode from base64
            decoded = base64.urlsafe_b64decode(pob_code)

            # Decompress
            xml_string = zlib.decompress(decoded).decode('utf-8')

            return xml_string
        except Exception as e:
            raise ValueError(f"Failed to decode PoB code: {str(e)}")

    def parse_xml(self, xml_string: str) -> Dict[str, Any]:
        """Parse PoB XML and extract build information"""
        try:
            root = ET.fromstring(xml_string)

            build_data = {
                'name': 'Imported Build',
                'class': 'Unknown',
                'ascendancy': 'None',
                'level': 100,
                'skills': [],
                'items': [],
                'tree': {},
                'notes': ''
            }

            # Extract build name
            build_elem = root.find('.//Build')
            if build_elem is not None:
                build_data['name'] = build_elem.get('name', 'Imported Build')
                build_data['class'] = build_elem.get('className', 'Unknown')
                build_data['ascendancy'] = build_elem.get('ascendClassName', 'None')
                build_data['level'] = int(build_elem.get('level', 100))

            # Extract skills
            skills_elem = root.find('.//Skills')
            if skills_elem is not None:
                for skill_set in skills_elem.findall('SkillSet'):
                    for skill in skill_set.findall('Skill'):
                        skill_info = {
                            'label': skill.get('label', 'Unnamed Skill'),
                            'enabled': skill.get('enabled', 'true') == 'true',
                            'slot': skill.get('slot', ''),
                            'gems': []
                        }

                        for gem in skill.findall('Gem'):
                            gem_info = {
                                'name': gem.get('nameSpec', 'Unknown'),
                                'level': gem.get('level', '20'),
                                'quality': gem.get('quality', '0'),
                                'enabled': gem.get('enabled', 'true') == 'true'
                            }
                            skill_info['gems'].append(gem_info)

                        if skill_info['gems']:
                            build_data['skills'].append(skill_info)

            # Extract items
            items_elem = root.find('.//Items')
            if items_elem is not None:
                for item_set in items_elem.findall('ItemSet'):
                    for slot in item_set.findall('Slot'):
                        slot_name = slot.get('name', '')
                        item_elem = slot.find('Item')
                        if item_elem is not None:
                            item_text = item_elem.text or ''
                            if item_text:
                                # Parse item name from first line
                                lines = item_text.strip().split('\n')
                                item_name = lines[0] if lines else 'Unknown Item'

                                build_data['items'].append({
                                    'slot': slot_name,
                                    'name': item_name,
                                    'raw': item_text
                                })

            # Extract passive tree
            tree_elem = root.find('.//Tree')
            if tree_elem is not None:
                spec_elem = tree_elem.find('Spec')
                if spec_elem is not None:
                    nodes = spec_elem.get('nodes', '')
                    build_data['tree'] = {
                        'nodes': nodes,
                        'url': spec_elem.get('treeVersion', ''),
                        'sockets': spec_elem.get('sockets', ''),
                    }

            # Extract notes
            notes_elem = root.find('.//Notes')
            if notes_elem is not None:
                build_data['notes'] = notes_elem.text or ''

            return build_data

        except ET.ParseError as e:
            raise ValueError(f"Failed to parse XML: {str(e)}")

    def parse_pob_code(self, pob_code: str) -> Dict[str, Any]:
        """Main method to parse a PoB code and return build data"""
        xml_string = self.decode_pob_code(pob_code)
        build_data = self.parse_xml(xml_string)
        self.build_data = build_data
        return build_data

    def get_leveling_milestones(self) -> List[Dict[str, Any]]:
        """Generate leveling milestones based on build data"""
        milestones = [
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

        return milestones
