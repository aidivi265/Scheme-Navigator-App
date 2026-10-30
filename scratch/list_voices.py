import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    for v in voices:
        loc = v.get('Locale', '')
        if '-IN' in loc or 'pa-' in loc or 'ur-' in loc or 'or-' in loc:
            print(v['ShortName'], '|', loc, '|', v['Gender'])

if __name__ == '__main__':
    asyncio.run(main())
