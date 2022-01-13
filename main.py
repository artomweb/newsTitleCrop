from cropScreen import crop
import asyncio
from pyppeteer import launch
import requests
from bs4 import BeautifulSoup


def main():
    word = "omicron"
    # articles = ["https://www.bbc.co.uk/news/education-59840634", "https://www.bbc.co.uk/news/uk-scotland-59851383",
    #             "https://www.bbc.co.uk/news/uk-northern-ireland-59849605", "https://www.bbc.co.uk/news/health-59840524", "https://www.bbc.co.uk/news/world-europe-guernsey-59839484"]

    baseUrl = "https://www.bbc.co.uk/search?q=omicron&page="

    articles = []
    for i in range(30):
        article = requests.get(baseUrl + str(i))

        soup = BeautifulSoup(article.text, 'html.parser')

        lists = soup.find_all(class_='ssrcss-v19xcd-Stack e1y4nx260')[0].find_all(
            "li")

        for l in lists:
            href = l.find_all("a")[0]["href"]
            if "news" in href and "articles" not in href:
                print(href)
                articles.append(href)

    print(articles)
    print(f"Length: {len(articles)}")
    getArticles(articles, "omicron")


def getArticles(articles, word):

    # articles = ["https://www.bbc.co.uk/news/world-europe-59948920",
    #             "https://www.bbc.co.uk/news/uk-england-59968307", "https://www.bbc.co.uk/news/health-59969785", "https://www.bbc.co.uk/news/uk-england-essex-59983193", "https://www.bbc.co.uk/news/uk-england-tees-59965761", "https://www.bbc.co.uk/news/uk-england-york-north-yorkshire-59967813", "https://www.bbc.co.uk/news/world-europe-59948920", "https://www.bbc.co.uk/news/uk-england-sussex-59953004", "https://www.bbc.co.uk/news/uk-scotland-scotland-business-59916356", "https://www.bbc.co.uk/news/uk-northern-ireland-59915018", "https://www.bbc.co.uk/news/uk-england-cambridgeshire-59907612", "https://www.bbc.co.uk/news/world-59901547", "https://www.bbc.co.uk/news/uk-northern-ireland-59916454", "https://www.bbc.co.uk/news/uk-england-stoke-staffordshire-59901883", "https://www.bbc.co.uk/news/uk-england-surrey-59898058", "https://www.bbc.co.uk/news/uk-scotland-59893246", "https://www.bbc.co.uk/news/world-asia-india-59890816", "https://www.bbc.co.uk/news/entertainment-arts-59889228",  "https://www.bbc.co.uk/news/uk-england-hampshire-59882944", "https://www.bbc.co.uk/news/world-middle-east-59853772", "https://www.bbc.co.uk/news/uk-59870825",  "https://www.bbc.co.uk/news/uk-england-lancashire-59868933", "https://www.bbc.co.uk/news/world-australia-59864428", "https://www.bbc.co.uk/news/health-59862568", "https://www.bbc.co.uk/news/world-africa-59832843",  "https://www.bbc.co.uk/news/uk-wales-59847816"]

    for article in articles:
        name = article.split("/")[-1]
        asyncio.get_event_loop().run_until_complete(saveScreenshot(article, name))
        found = crop(f'articles/{name}.png', name, word)
        if found:
            print(f"found {word} in {article}")
        else:
            print(f"could not find {word} in {article}")


async def saveScreenshot(articleURL, name):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({
        "width": 1920,
        "height": 1080,
        "deviceScaleFactor": 2,
    })
    await page.goto(articleURL)
    await page.screenshot({'path': f'articles/{name}.png'})
    await browser.close()


if __name__ == '__main__':
    main()
