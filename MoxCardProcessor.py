import scrython
import re
import os
import requests
import random

class CardProcessor:
    name = ""
    quantity = ""
    set_code = ""
    collector_number = ""


    @staticmethod
    def parse_card(card, fallback = True):
        card = card.strip()
        if not card:
            return False # Bad input
        # Regex to extract quantity, card name, set code, collector number (optional)
        print("Parsing card info...")
        match = re.match(r'^(\d+)\s+(.+?)\s+\((\w+)\)\s+(.+)$', card)
        if match:
            print("Found all info!")
            CardProcessor.quantity = match.group(1)
            CardProcessor.name = match.group(2)
            CardProcessor.set_code = match.group(3)
            CardProcessor.collector_number = match.group(4)
        elif fallback:
            print("Parse failed --> fallback: try to extract quantity and name only")
            parts = card.split(' ', 1)
            CardProcessor.quantity = parts[0] if parts else ''
            CardProcessor.name = parts[1] if len(parts) > 1 else card
            CardProcessor.set_code = ''
            CardProcessor.collector_number = ''
        else:
            return False # OK input, but fallback mode disabled
        return True # Good input

    @staticmethod
    def get_oldest_set_cards(card_list_str):
        cards = card_list_str.strip().split('\n')
        results = []
        for card_entry in cards:
            if CardProcessor.parse_card(card_entry) == False:
                continue
            
            # Search for all printings
            # Query Scryfall for each card by name
            try:
                results.append(CardProcessor.get_oldest_card_version(CardProcessor.quantity, CardProcessor.name))
                print("found oldest version!")
            except Exception:
                results.append(f"{CardProcessor.quantity}x {CardProcessor.name} NOT FOUND")
                print("failed to find card :(")
        return '\n'.join(results)

    @staticmethod
    def get_oldest_card_version(quantity, card_name):
        try:
            search = scrython.cards.Search(q=f'!"{card_name}"', order='released', dir='asc', unique='prints')
            if search.total_cards() > 0:
                card = search.data()[0]
                name = card['name']
                set_code = card['set'].upper()
                collector_number = card['collector_number']
                return (f"{quantity} {name} ({set_code}) {collector_number}")
            else:
                return (f"1 {card_name} NOT FOUND")
        except Exception:
            return (f"1 {card_name} NOT FOUND")
        
    @staticmethod
    def download_mtg_images_scrython(card_list_str: str, output_path: str):
        """
        Downloads MTG card images using scrython from a formatted string.
        
        Format: "[Quantity] [Card Name] ([Set Code]) [Collector Number]"
        """

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        #pattern = r'^(\d+)\s+(.+?)\s+\((\w+)\)\s+(\d+)$'
        for line in card_list_str.strip().splitlines():
            # match = re.match(pattern, line.strip())
            # if not match:
            #     print(f"Skipping invalid line: {line}")
            #     continue

            if CardProcessor.parse_card(line, False) == False:
                print(f"Skipping invalid line: {line}")
                continue

            #quantity, name, set_code, collector_number = match.groups()
            #quantity = int(quantity)

            try:
                card = scrython.cards.Collector(code=CardProcessor.set_code, collector_number=CardProcessor.collector_number)
                image_url = card.image_uris()['large']
            except Exception as e:
                print(f"Error fetching {CardProcessor.name} ({CardProcessor.set_code}) {CardProcessor.collector_number}: {e}")
                continue

            safe_name = re.sub(r'[\\/*?:"<>|]', '', CardProcessor.name)
            filename = f"{safe_name}_{CardProcessor.set_code}_{CardProcessor.collector_number}.jpg"
            filepath = os.path.join(output_path, filename)

            try:
                img_data = requests.get(image_url).content
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                print(f"Saved: {filename}")
            except Exception as e:
                print(f"Error saving {filename}: {e}")

    @staticmethod
    def createPacks(card_string, packSize):

        card_list = []
        for line in card_string.strip().splitlines():
            if CardProcessor.parse_card(line) != False:
                for i in range(int(CardProcessor.quantity)):
                    card_list.append(CardProcessor.name)
            else:
                print("Error resolving card: " + line)

        packCount = 0
        packContents = ""

        uIn = input("Would you like it printed to a .txt file (Packs.txt in this directory) or to the console? (Y for .txt, enter anything else for console print): ")
        
        while card_list:
            packCount += 1

            packContents += "\nPack #" + str(packCount) + "\n"

            for pack in range(packSize):
                if(len(card_list) != 1 and len(card_list) != 0):
                    randCard = random.randint(0, len(card_list) - 1)
                elif(len(card_list) == 1):
                    randCard = 0
                else:
                    break
                packContents += card_list[randCard] + "\n"
                card_list.pop(randCard)
            
            packContents += "\n"
            
            if uIn != "Y":
                print("\nPack #" + str(packCount) + "\n" + packContents + "\n")
            
            else:
                quantities_file = os.path.join(os.path.dirname(__file__), "Packs.txt")
                with open(quantities_file, "w") as f:
                    i = 0
                    for line in packContents.strip().splitlines():
                        f.write(f"{line}\n")  # Space for user to type quantity
                        i += 1

def main():

    card_string = ""

    strIn = ""

    strIn = input("Input list of cards (type -1 to finish list or ? for usage info): ")

    while strIn != "-1":
        
        if strIn != "-1" and strIn != "?":
            card_string += strIn + "\n"
        else:
            print("""
                Input a list of cards in the following format:
                
                    1 Academy Rector (UDS) 1
                    1 Adarkar Wastes (BLC) 291
                    1 Aftershock (PLST) TMP-160
                
                This is the exact format that you see if you open one of your own Moxfield decks then hit \"Bulk Edit\".

                As a final note, when you want to finish typing your card list, make sure to type only -1 with no spaces, avoiding cases such as \" -1\" or \"-1 \".
                This confuses the script and makes it think you're still typing cards. Nothing catastrophic happens though, it's just that when it 
                tries to parse its card information, it just throws an error for the card in your final output. Feel free to go ahead and just paste in your list now or type -1 to quit.\n""")
        
        strIn = input()

    uIn = input("Would you like to use the oldest prints? (Y to confirm, enter anything else to skip): ")

    if uIn == "Y":
        card_string = CardProcessor.get_oldest_set_cards(card_string)
        print("\nDone!\n\n" + card_string)

    uIn = input("Would you like to download the images for your cards? (Y to confirm, enter anything else to skip): ")

    if uIn == "Y":
        path_name = input("Where would you like the images saved? (Full path): ")

        if os.path.exists(path_name):
            CardProcessor.download_mtg_images_scrython(card_string, path_name)
        else:
            while(os.path.exists(path_name) == False):

                print("Invalid Path, please reinput: ")

                path_name = input()

                if os.path.exists(path_name):
                    CardProcessor.download_mtg_images_scrython(card_string, path_name)

    uIn = input("Would you like to generate random packs with this list? (Y to confirm, enter anything else to skip): ")

    if uIn == "Y":
        
        packNum = int(input("How many cards per pack?: "))

        while isinstance(packNum, int) == False or packNum <= 0:
            packNum = int(input("Invalid Number, plese reinput: "))

        CardProcessor.createPacks(card_string, packNum)
            

    input("\nPress Enter key to quit.\nPS: Thanks for using my script! -Fresh")
    
if __name__ == "__main__":
    main()

