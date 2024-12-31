def convert_subs_to_links(input_file, output_txt):
    with open(input_file, 'r', encoding='utf-8') as file:
        next(file)
        
        links = []
        for line in file:
            if(line.strip()):
                parts = line.split(',')
                if(len(parts) >= 2):
                    channel_url = parts[1].strip()
                    if(channel_url):
                        links.append(channel_url)

    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        for link in links:
            txt_file.write(link + '\n')

if(__name__ == "__main__"):
    input_file = "subscriptions.csv"
    output_file = "channel_links.txt"
    
    convert_subs_to_links(input_file, output_file)
    print(f"Channel links have been saved to {output_file}") 