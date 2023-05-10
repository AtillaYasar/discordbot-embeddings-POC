import discord
from discord.ext import commands
import embeddings_module
import io, json

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emb_user = EmbeddingsUser()
    
    def embsearch(self, text):
        params = {
            'n':3,
            'hasno':['search term'],
            'has':[],
        }
        embedded_term = self.emb_user.get_embedding(text)
        res = self.emb_user.search(embedded_term, params)
        return res
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            res = self.embsearch(message.content)
            print(res)

            '''# send message.txt
            to_send = json.dumps(res, indent=4)
            ctx = message.channel

            output = io.StringIO(to_send)
            await ctx.send("text related to your input:", file=discord.File(output, filename='message.txt'))
            output.close()'''
            for item in res:
                await message.channel.send('\n'.join([
                    f'score: {item["score"]}',
                    item['text'],
                    '-'*20,
                ]))
        else:
            pass

class EmbeddingsUser:
    def __init__(self):
        self.data_handler = embeddings_module.DataHandler()

    def search(self, embedded_term, params):
        return self.data_handler.search(embedded_term, params)

    def get_embedding(self, text):
        return self.data_handler.get_embedding(text)

    def embed_list(self, lst, metadata):
        self.data_handler.embed_list(lst, metadata)

embeddings_user = EmbeddingsUser()
raw = '''
# Introduction
> The AI has been trained on a vast amount of audiobooks, and to a lesser extent, podcasts. This is the context it understands the best, and it provides the most predictable results when generating voiceovers. If you write something in the style of a book, the AI can sometimes interpret how to perform a certain passage from the context of the writing itself. To achieve a more emotive vocal range, you can lower the stability slider, although this may sacrifice some degree of predictability.
=====
# Emotion
> If you want the AI to express a specific emotion, the best approach is to write in a style similar to that of a book. To find good prompts to use, you can flip through some books and identify words and phrases that convey the desired emotion.
> For instance, you can use dialogue tags to express emotions, such as “he said, confused”, or “he shouted angrily”. These types of prompts will help the AI understand the desired emotional tone and generate a voiceover that accurately reflects it. With this approach, you can create highly customized voiceovers that are perfect for a variety of applications.
```"Are you sure about that?" he said, confused.
"Don’t test me!" he shouted angrily.```
=====
# Pacing
> Based on my own testing, which contradicts some information out there, I believe that when you use multiple samples in a clone, the AI puts them back-to-back without any space between them. This can lead to pacing issues and cause the AI to talk faster than it should. This is likely why some people have reported fast-talking clones.
> To control the pacing of the speaker, you can use the same approach as in emotion, where you write in a style similar to that of a book. While it's not a perfect solution, it can help improve the pacing and ensure that the AI generates a voiceover at the right speed. With this technique, you can create high-quality voiceovers that are both customized and easy to listen to.
```"I wish you were right, I truly do, but you're not," he said slowly.```
=====
# Pause
> Personally, the one trick I use the most to control when to pause and to get longer pauses is a simple dash (-) or the em-dash (—).
```"It - is - getting late."```
> Ellipsis (...) also work to add a pause between words but usually, for me at least, also adds some "hesitation" or "nervousness" to the voice that might not always fit.
```""I... yeah, I guess so...""```
> The system is always being improved upon, and ElevenLabs are currently working on adding features such as the ability to add pauses and change the speed of the generated voiceovers.
> Currently, you can add a pause by using the MLSS tag <break time="3000" />, where the number is the length of the pause in milliseconds (1000ms = 1s). This will insert a pause of the specified duration into the generated voiceover.
> Alternatively, you can achieve a pause by inserting a line break or two where you want the pause to occur. The AI will often recognize the change in the text and adapt accordingly, resulting in a natural-sounding pause. With these techniques, you can customize your voiceovers even further and create highly polished content that meets your specific needs.
```Welcome

to this guided meditation.

Find a comfortable seated position, 

with your back straight and your feet on the ground.```
=====
# Cloning Voices
> When cloning a voice, it's important to consider what the AI has been trained on – English audiobooks in this case – and the quality of the audio used to train the AI. The AI can handle some accents, like American, British, and Australian, but it's best at replicating American and British accents. If you have an accent that falls outside of these, the AI might have a hard time replicating your voice perfectly and may give you a slightly different accent.
> The audio quality is more important than the length of audio. About 1 minute of clear audio without any artefacts or background noise of any kind seem to be the sweet spot at the moment. The AI will try to mimic the speed of the person talking as well as the inflections, so giving it a slower speaking voice with clear pronunciation seems to give better and more natural results.
=====
Do we plan to support more languages?
Yes, our priority at the moment is to support more popular spoken languages - from Spanish, German, French, Polish, Italian and Portuguese.
=====
Is voice conversion being developed?
Multilingual voice conversion is in the works, there is no planned release for it yet.
=====
My voice isn’t similar at all / monotonous / too chaotic, what is going on?
Our model uses a generative system, which means each result is different. To control the direction of the system, you can change the sliders in the “Voice Settings” tab or add more samples.
=====
What are the sliders in the “Voice Settings” tab?
The sliders provide a way of controlling your voice before generating, the stability slider aids in the emotional range of the voice while clarity aids in voice similarity.
=====
What is the ideal sample length for generating audio?
Generally, you’ll want no more than five minutes of sample audio composed of 30s-60s clips.
=====
I am a developer and I would like to use one of ElevenLabs services in my solution - how can I do it?
You can use our API, which is more explained here: https://docs.elevenlabs.io/
If you have a more specific question, you can ask around #api-forum.
=====
I just got billed but my quota has not yet been updated. Why?
It will take an hour or so for the system to sync with the payment. If you still don't see your updated quota after a few hours, please contact ElevenLabs directly.
=====
Can I safely use a voice I've cloned on ElevenLabs?
Here's a general summary of what you can and can't do: https://beta.elevenlabs.io/education.
If you are still unsure, please check with the proper authorities / copyright laws in your country.
=====
I do not have a credit card, or money, what can I do?
We are sorry to hear that. Free trial is available for Starter tier to try things out, no money needed. If you do not have a credit card at all, then all you can use is a "Free tier".
We understand that the "Free tier" is quite limited. We will be adding some more things to Free tier in the future, like Voice Design (not Voice Lab). We are a business and a Free tier is costing us a lot of money already to support, and was heavily abused by 4Chan and others when it had less restrictions.
=====
I’ve run into an error, have a problem with my account, or lost purchased characters.
Send a message in #support-forum or post on https://feedback.elevenlabs.io/ depending on your issue, one of our moderators will do their best to assist you. If you want to contact us privately, write to our email: team@elevenlabs.io
'''[1:-1]

lst = raw.split('\n=====\n')
embeddings_user.embed_list(lst, metadata=[['elevenlabs'] for _ in lst])