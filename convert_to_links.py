def convert_csv_to_links(input_file, output_txt):
    with open(input_file, 'r', encoding='utf-8') as file:
        next(file)
        
        links = []
        for line in file:
            if(line.strip()):
                video_id = line.split(',')[0].strip()
                video_id = video_id.strip(' -')
                if(video_id):
                    link = f"https://www.youtube.com/watch?v={video_id}"
                    links.append(link)

    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        for link in links:
            txt_file.write(link + '\n')

if(__name__ == "__main__"):
    input_file = "Watch later-videos.csv"
    output_file = "youtube_links.txt"
    
    convert_csv_to_links(input_file, output_file)
    print(f"Links have been saved to {output_file}") 