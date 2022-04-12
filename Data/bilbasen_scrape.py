# Importing the SitemapSpider for crawling the webpage.
from scrapy.spiders import SitemapSpider

# Creating class with relevant extractions properties.
class BilbasenWebScrape(SitemapSpider):
    # Naming the spider.
    name = 'bilbasen'
    
    # Defining the sitemap on which URLs are listed.
    sitemap_urls = ['http://www.bilbasen.dk/sitemap_carsLatest.axd']
    
    # Initiaing each iteration with a slight delay to avoid abusing the site's servers.
    DOWNLOAD_DELAY = 0.2 
    
    # Defining properties to be extracted.
    def parse(self, response):
            yield {
                'make_model': response.xpath('//*[@id="bbVipTitle"]/span/text()').extract_first(),
                'sub_model': response.xpath('//*[@id="bbVipTitle"]/text()').extract_first(),
                'aargang': response.xpath('//*[@id="bbVipYearInfo"]/div[3]/span[2]/text()').extract_first(),
                
                'url': response.request.url,
                
                'nypris': response.css('td.selectedcar::text')[0].extract(),
                'hestrekaefter_torque': response.css('td.selectedcar::text')[1].extract(),
                '0-100kmt': response.css('td.selectedcar::text')[2].extract(),
                'tophastighed': response.css('td.selectedcar::text')[3].extract(),
                'km_l': response.css('td.selectedcar::text')[4].extract(),
                'bredde': response.css('td.selectedcar::text')[5].extract(),
                'laengde': response.css('td.selectedcar::text')[6].extract(),
                'hoejde': response.css('td.selectedcar::text')[7].extract(),
                'lasteevne': response.css('td.selectedcar::text')[8].extract(),
                'traekhjul': response.css('td.selectedcar::text')[9].extract(),
                'cylindre': response.css('td.selectedcar::text')[10].extract(),
                'ABS-bremser': response.css('td.selectedcar::text')[11].extract(),
                'max_paahaeng': response.css('td.selectedcar::text')[12].extract(),
                'airbags': response.css('td.selectedcar::text')[13].extract(),
                'esp': response.css('td.selectedcar::text')[14].extract(),
                'tank': response.css('td.selectedcar::text')[15].extract(),
                'gear': response.css('td.selectedcar::text')[16].extract(),
                'geartype': response.css('td.selectedcar::text')[17].extract(),
                'vaegt': response.css('td.selectedcar::text')[18].extract(),
                'doere': response.css('td.selectedcar::text')[19].extract()
                }
            
