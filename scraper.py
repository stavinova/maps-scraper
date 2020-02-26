# -*- coding: utf-8 -*-
from googlemaps import GoogleMapsScraper
from datetime import datetime, timedelta
import argparse
import csv
HEADER = ['place', 'id_review', 'caption', 'timestamp', 'rating', 'username', 'n_review_user', 'n_photo_user', 'url_user']

def csv_writer(path='data/', outfile='gm_reviews.csv'):
    targetfile = open(path + outfile, mode='w', encoding='utf-8', newline='\n')
    writer = csv.writer(targetfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(HEADER)

    return writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Maps reviews scraper.')
    parser.add_argument('--N', type=int, default=100, help='Number of reviews to scrape')
    parser.add_argument('--i', type=str, default='urls.txt', help='target URLs file')
    parser.add_argument('--place', dest='place', action='store_true', help='Scrape place metadata')
    parser.set_defaults(place=False)

    args = parser.parse_args()

    with GoogleMapsScraper() as scraper:
        with open(args.i, 'r', encoding = "utf-8") as urls_file:
            writer = csv_writer()
            for name in urls_file:
                print(name)
                if args.place:
                    print(scraper.get_account(name))
                else:
                    url = scraper.get_place_url(name)
                
                    error = scraper.sort_by_date(url)
                    if error == 0:
                        # store reviews in CSV file
                        
                        
                        n = 0
                        
                        while n < args.N:
                            #leng = scraper.get_num_reviews()
                            reviews = scraper.get_reviews(n)
                            if len(reviews) > 0:
                                for r in reviews:
                                    writer.writerow([name.split(';')[1]] + list(r.values()))

                                n += len(reviews)
                                print(n)
                            else:
                                break
                            
