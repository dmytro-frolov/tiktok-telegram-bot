import re
import requests

from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackContext

from bs4 import BeautifulSoup
import html

def get_link(html, link_name='playAddr'):
    pattern = f'{link_name}":"(.*?)"'
    a = re.findall(pattern, html)
    print()


def tt_handler(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': 'ttwid=1%7CeLqe70PJDJIHuKIRcK3OeAcJgQdKqyXMW_A5_c22YvQ%7C1643563609%7C9129956c2e4ea50189d0c3c33f32d5659aee6cc2fd3b1c934c655ff773d3888f; msToken=NI1xFGz3hGvSZm2exx2p88GmIFc-eLT5_3ILp3Q43kzzLZKknJix93ri2rCSbMx_4Nc4rDdf8CssvOcsEUAiP0hzWc0DpDlJASWtjwPSAPGQhlJ2wxTiSDoJoU6HWVVI; _abck=6C288CB92B2F42F3B97F12DF8D11A060~-1~YAAQDSkZTmNN65B+AQAAI/H3qwdUfoHO8Y1T6XQTSdw7fu1kddDx3uW8i3n2t42BU541hejA9H7CLGNUzbiIGhQETi+N8FCJ7pIS97dBbEN5IjqVJdIuwOhezyx/AtxOzINnO8NNqVZk/fxsjAjcbqneZv4PyzCIR+pzCShRu5kCuB8JzZSwn3NYQFpY5DQjjj2LO2sIGOo4rvUEU0kY2ELSKl1nDoklmlNxPuTdkMeRt6xboD8ZIem/YFDsc3c02+Sw1W91iClTv6wu38qF/fIsuaC4aqPaiZIjGme6ydgEj8Fc7pVMc+UiW5NnYXuYBHWY5IVgnB0TUydFRgBshcUj8fpO41F2HWR0JGzoyR8OgzCdjq8zaF8noJqWrwBbEMx4kQHbTe+IC3g=~-1~-1~-1; tt_csrf_token=mo6HJz8kvoAlMZuHpdVtEoTT; bm_sz=B66B08FC60828594B6608424FFB149A6~YAAQDSkZTmRN65B+AQAAI/H3qw6QXxYsaZjOR1EQnhF4APcRvCpOPOVWj1tHVFOD7yAxuGmkzZWWQTzzLVJD+iKv8h0OhoF6jKezDI5ZwP2MDxDXvpKBOv9EVjhYiXWzbzYYNVST8VGNijZsSKowfgRvmcsV0mAEwv8jmF4EMOdHLJA9jNpdjgZZUnvfEaw0TpESBVaqLCY3/n2t6OnQde476u7eUZrJbNrDbC5sPv3jl0CwRnw6hJ2ur2qUQB0/dDNfpU/lh5Pt/DKcKn2aLFqnDhhq6Jolu3b3TOZ7jMMdGjs=~3748674~3228976; ak_bmsc=6EC8F4A0EDD4096B526F9DBFC528397F~000000000000000000000000000000~YAAQDSkZTmVN65B+AQAA/vP3qw4Gcwh3gvGVeUWmv/cvgCTpgGBEkm05PKhlaBq5KHXz2UzccZ5nIhon2RsA6INmb8aS3s+NyC7TMnbkC8oEY3MUhqAXVxbr2Y6VSDbS8sOzf8hJV4YxYfTusB9BysWK/cXjOz3TFhQzLjI0tDq9BlPr/22bnywL/1p2kwjEa6Pudkzv3vVYeh4DqjIoWhuQfY23EEHGzEjA55To/G6ad+pUrsRUwwxR7TeaAPSpxOSHRat7Dosj1PnB/9aW+FX+DP9LBBELgpJEpmvwZiNxhzRGg13VwyV0I/wRRMpbYUC7ulHYiDQ1HGdXzY5hKqvgRcXC1iWW207L5QNFMR79I4h2KfK/EKsEIbcPeuMYU1KkgOLoywX5yA==; bm_sv=EEAA1E94859DBB63EEDBFFF256213019~66TObEtQNeFIn9ic/bd8bZ/goz0fYCTnBwpENwFQoLakZa4+m/+J2MzUw1JxWqsAIA8hX+CN0m1xIftD+ffmGLKxsHPGtT2plgGumB4tR0reVRlf/zgh2+1jD3YnrGjJwQFUVMGzCgIEVHpSlgTAjmkGqJiw7Ar5jJ0thHO5JWQ=; bm_mi=1E634BD10F47B1C6638C27CA9C3F4024~4D6Yxpacz3fqkvyz7WBYo/ag+nOtRxVfeLDGxlToyFEBnpSMSY8dJC7WXF9qiP83+2zhk+vC8Q2PPhRStGLFlMMRoQVvlnonLPj+paBUuTZxZtyyBeTQoR5zr34434RFed8AQFWWcxn6jdykT+QRNU3ZPK2sbYpk5NsQsOqOEYpA6b6dnkNEbm3HtMPQjuCZD3UFygZHCCK/a8oHzjCh8MP5Jt48JZ0hxx61wE7ZsWGKhiY1RAmmFW6eHiABAR0YhRa3bSxMCfNqbVT38fQlu8JDVmtr6EkqFM2ts2jeSgY=; bm_mi=1E634BD10F47B1C6638C27CA9C3F4024~4D6Yxpacz3fqkvyz7WBYo/ag+nOtRxVfeLDGxlToyFEBnpSMSY8dJC7WXF9qiP83+2zhk+vC8Q2PPhRStGLFlOoqPEvF9r7VDbmgW6AZMgHZDV91r1oyd2agYMRRNYouuCNA5VBTDqU7FgYP5pNejaw1EogoVimwzjks+rNhZ+daowcqxtYYfQDger2u3ozhT+3ZC6CGTCmAtVUlhS2fzeYSkjXJ4lThLm1AIf5FdnEMz+EhpqacXhHsCd44gEJyEJDku1AngtVyFBhsv+VbqIBFXQAaqbauBnl6yj+W7Zg=; bm_sv=EEAA1E94859DBB63EEDBFFF256213019~66TObEtQNeFIn9ic/bd8bZ/goz0fYCTnBwpENwFQoLakZa4+m/+J2MzUw1JxWqsAIA8hX+CN0m1xIftD+ffmGLKxsHPGtT2plgGumB4tR0rL3oR27NHPlsI7Vgw3G7/qe05ZOMp3M+dc3tlnTZIHL1jqbq3tWMx2Ix1571dGWOg=; msToken=edpo0BxuDDdR9q6Epi0pW8hWLn60lPjeDlEN3sRXYgGPr-JtmhD4WF-E29NZ1FHnBqWHlrPpOV2A6x9J5xTYq2sK7odeNVmCiY73O0qymqDUmiUfUZisZxLY-6E=',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Sec-GPC': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    response = requests.request("GET", link, headers=headers)

    html = response.text
    print(html.unescape(response.content.decode('ansi')))
    return get_link(html)



def handler(update: Update, context: CallbackContext):
    input_text = update.message.text
    if re.match("https://.*tiktok.com.*", input_text):
        output_text = tt_handler(input_text)

    else:
        output_text = input_text + ' durak'
    context.bot.send_message(chat_id=update.effective_chat.id, text=output_text)


MESSAGE_HANDLER = MessageHandler(Filters.text & (~Filters.command), handler)


#https://vm.tiktok.com/ZMLLVUE59/