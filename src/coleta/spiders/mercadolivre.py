import scrapy

#pip install selenium
#pip install webdriver-manager

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    def parse(self, response):
        # Verifica se a requisição foi bem-sucedida
        if response.status == 200:
            products = response.css('div.ui-search-result__content')
            self.log(f'Número de produtos encontrados: {len(products)}')

            for product in products:

                prices = product.css('span.andes-money-amount__fraction::text').getall()
                cents = product.css('span.andes-money-amount__cents::text').getall()

                yield{
                    'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                    'name' : product.css('h2.ui-search-item__title::text').get(),
                    'old_price_reais': prices[0] if len(prices) > 0 else None,
                    'old_price_centavos': cents[0] if len(cents) > 0 else None,
                    'new_price_reais': prices[1] if len(prices) > 1 else None,
                    'new_price_centavos': cents[1] if len(cents) > 1 else None,
                    'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                    'reviews_amount': product.css('span.ui-search-reviews__amount::text').get()
                }

        if self.page_count < self.max_pages:
            #vamos fazer um parses do botão "proxima pagina"
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                #queremos que após entrar na proxima pagina ele realize o parse novamente para pegar todos os itens
                yield scrapy.Request(url=next_page, callback=self.parse)

        else:
            self.log(f'Erro ao acessar a página: {response.status}')


       