
import scrapy

class BayutSpider(scrapy.Spider):
    name = 'bayut_spider'
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']
    max_properties = 3500

    def __init__(self, *args, **kwargs):
        super(BayutSpider, self).__init__(*args, **kwargs)
        self.property_count = 0

    def parse(self, response,**kwargs):
        property_urls = response.css('a._287661cb::attr(href)').getall()

        for url in property_urls:
            yield response.follow(url, callback=self.parse_details)
            self.property_count += 1
        if self.property_count >= self.max_properties:
            return

        next_page = response.css('[title="Next"]::attr(href)').get()
        if next_page is not None and self.property_count < self.max_properties:
            next_page_url = 'https://www.bayut.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_details(self, response):
        for data in response.css('div._6803f627'):
            for data1 in response.css('div._607ecfd5._3532643f'):
                for data2 in response.css('div._74ac503e'):
                    for data3 in response.css('div._31cc6dcd'):
                        # for data4 in response.css('div._1075545d._48209818.d059c029'):

                        yield {
                            'Property_id': data.css('span._812aa185::text').getall()[2],
                            'Purpose': data.css('span._812aa185::text').getall()[1],
                            'Type': data.css('span._812aa185::text').getall()[0],
                            'added_on': data.css('span._812aa185::text').getall()[5],
                            'furnishing': data.css('span._812aa185::text').getall()[3],
                            # 'Price': ' '.join(data.css('span.e63a6bfb::text, span._105b8a67::text, span._56562304::text').getall()),
                            'price': {
                                'currency': data.css('span.e63a6bfb::text').get(),
                                'amount': data.css('span._105b8a67::text').get(),
                            },
                            'Location': data.css('div._1f0f1758::text').get(),
                            # 'bed_bath_size': ' '.join(data.css('span.fc2d1086::text').getall()),
                            'bed_bath_size': {
                                'bedrooms': data.css('span.fc2d1086::text')[0].get(),
                                'bathrooms': data.css('span.fc2d1086::text')[1].get(),
                                'size': data.css('span.fc2d1086 span:nth-child(1)::text').get(),
                            },
                            # 'Permit_number': data.css('span._812aa185[aria-label="Permit Number"]::text').get(),

                            'agent_name': data1.css('a.f730f8e6::text').get(),
                            'aminities': data.css('span._005a682a::text').getall(),
                            'breadcrumbs': data2.css('span._327a3afc::text').getall(),
                            'image_url': data3.css('img::attr(src)').get(default=''),
                            'description': data.css('span._2a806e1e::text').getall(),

                        }







# import scrapy
#
# class BayutSpider(scrapy.Spider):
#     name = 'bayut'
#     start_urls = [
#         'https://www.bayut.com/to-rent/property/dubai/'
#     ]
#
#     def parse(self, response,**kwargs):
#         properties = response.css('*[aria-label*="Link name"]')
#         for property in properties:
#             property_id = property.css('span[aria-label*="Link name"]::text').get()
#             yield {'propertyid': property_id}


        # def parse(self, response):
        #     properties = response.css('[aria-label="property-item"]')
        #     for property in properties:
        #         property_id = property.css('span[aria-label="property-id"]::text').get()
        #         yield {'propertyid': property_id}




# import scrapy
# #
# class BayutSpiderSpider(scrapy.Spider):
#     name = "bayut_spider"
#     allowed_domains = ["bayut.com"]
#     start_urls = ['https://www.bayut.com/to-rent/property/dubai/']
#
#     def parse(self, response, **kwargs):
#         purpose = response.css('div._22f85495::text').get()
#
#         for properties in response.css('li.ef447dde'):
#             yield {
#                 'purpose':properties.css('div._22f85495::text').get()
#
#             }



# ---------------------------------------------------------------------------
#
# import scrapy
#
#
# class BayutSpiderSpider(scrapy.Spider):
#     name = "bayut_spider"
#     allowed_domains = ["bayut.com"]
#     start_urls = ['https://www.bayut.com/to-rent/property/dubai/']
#
#     def parse(self, response, **kwargs):
#         type = response.css('span._812aa185[aria-label="Type"]::text').get()
#         address = response.css('div._1f0f1758::text').get()
#         addedon = response.css('span._812aa185[aria-label="Reactivated date"]::text').get()
#         furnish = response.css('span._812aa185[aria-label="furnishing"]::text').get()
#
#         for purpos in response.css('div._22f85495::text'):
#             purpose = response.css('div._22f85495::text').get()
#
#             yield {
#                 'purpose': purpose.strip() if purpose else '',
#                 'type': type.strip() if type else 'Type',
#                 'added_on': addedon.strip() if addedon else 'Reactivated date',
#                 'furnishing': furnish.strip() if furnish else 'furnishing',
#                 'address': address.strip() if address else '',
#             }



# new method

# import scrapy
#
# class BayutSpiderSpider(scrapy.Spider):
#     name = "bayut_spider"
#     allowed_domains = ["bayut.com"]
#     start_urls = ['https://www.bayut.com/to-rent/property/dubai/','https://www.bayut.com/property/details-6643645.html']
#
#     def parse(self, response,**kwargs):
#
#
#         for data in response.css('li.ef447dde'):
#             for data1 in response.css('main'):
#
#                 yield {
#
#                     'prop_id': data1.css('span._812aa185::text').get(),
#                     'purpose': data1.css('span._812aa185 span:nth-child(3)::text').get(),
#                     'Type': data1.css('span._812aa185 span:nth-child(1)::text').get(),
#                     'added_on': data1.css('span._812aa185 span:nth-child(4)::text').get(),
#                     'furnishing': data1.css('span._812aa185 span:nth-child(2)::text').get(),
#                     # 'price': {
#                     #     data.css('span.f343d9ce::text').get(),
#                     #     data.css('span.c2cc9762::text').get(),
#                     # },
#                     'price': {
#                         data.css('span.c2cc9762::text').get() +' '+ data.css('span.f343d9ce::text').get() + ' '+ data.css('span.e76c7aca::text').get()
#                     },
#
#                     'Location': data.css('div._7afabd84::text').get(),
#                     'size,bath,bed': {
#                         'square_feet': data.css('div._22b2f6ed span:nth-child(1)::text').get(),
#                         'bathroom': data.css('div._22b2f6ed span:nth-child(3)::text').get(),
#                         'bedroom': data.css('div._22b2f6ed span:nth-child(2)::text').get()
#                     },
#
#                     'permit_number': data.css('div.c4fc20ba::text').get(),
#                     'Agent_name': data1.css('a.f730f8e6::text').get(),
#                     'image_url': data.css('div.c4fc20ba::text').get(),
#                     'Bread_crumbs': data.css('div.c4fc20ba::text').get(),
#                     'aminities': data.css('div.c4fc20ba::text').get(),
#                     'details': data1.css('span._2a806e1e::text').get(),


                # }

#
# import scrapy
#
#
# class BayutSpider(scrapy.Spider):
#     name = 'bayut_spider'
#     start_urls = ['https://www.bayut.com/to-rent/property/dubai/']
#
#
#     def parse(self, response,**kwargs):
#         property_urls = response.css('a._287661cb::attr(href)').getall()
#
#         for url in property_urls:
#             yield response.follow(url, callback=self.parse_details)
#
#         next_page_url = response.css('a.b7880daf::attr(href)').get()
#         if next_page_url:
#             yield response.follow(next_page_url, callback=self.parse)
#
#     def parse_details(self, response):
#         for data in response.css('div._6803f627'):
#             for data1 in response.css('div._607ecfd5._3532643f'):
#                 for data2 in response.css('div._74ac503e'):
#                     for data3 in response.css('div._31cc6dcd'):
#                         # for data4 in response.css('div._1075545d._48209818.d059c029'):
#
#                         yield {
#                             'Property_id': data.css('span._812aa185::text').getall()[2],
#                             'Purpose': data.css('span._812aa185::text').getall()[1],
#                             'Type': data.css('span._812aa185::text').getall()[0],
#                             'added_on': data.css('span._812aa185::text').getall()[5],
#                             'furnishing': data.css('span._812aa185::text').getall()[3],
#                             # 'Price': ' '.join(data.css('span.e63a6bfb::text, span._105b8a67::text, span._56562304::text').getall()),
#                             'price': {
#                                 'currency': data.css('span.e63a6bfb::text').get(),
#                                 'amount': data.css('span._105b8a67::text').get(),
#                             },
#                             'Location': data.css('div._1f0f1758::text').get(),
#                             # 'bed_bath_size': ' '.join(data.css('span.fc2d1086::text').getall()),
#                             'bed_bath_size': {
#                                 'bedrooms': data.css('span.fc2d1086::text')[0].get(),
#                                 'bathrooms': data.css('span.fc2d1086::text')[1].get(),
#                                 'size': data.css('span.fc2d1086 span:nth-child(1)::text').get(),
#                             },
#                             'Permit_number': data.css('span._812aa185[aria-label="Permit Number"]::text').get(),
#
#                             'agent_name': data1.css('a.f730f8e6::text').get(),
#                             'aminities': data.css('span._005a682a::text').getall(),
#                             'breadcrumbs': data2.css('span._327a3afc::text').getall(),
#                             'image_url': data3.css('img::attr(src)').get(default=''),
#                             'description': data.css('span._2a806e1e::text').getall(),
#
#                         }




