# Kekbot

Kekbot is a silly bot :robot: for Twitch chat. It converts Twitch and BTTV emotes, or pictures from an url into braille art. For now you can meet Kekbot on [@Damidema](https://www.twitch.tv/damidema) stream and redeem a braille art with 100 channel points.
Kebot also likes memes and it can produce AI generated copypastas. They are rarely meaningful, but sometimes funny :laughing:.

## How braille emotes work

Kekbot knows the most common Twitch and BTTV emotes. It can access to the emote if you use the **!kekthis** or the **!kekthat** command followed by the emote name (<ins>emote names are case sensitive!</ins>). 
With this method you can spam the braille version of more than 8000 different emotes! However not all of the emotes are available (for now).<br/>
Channel-specific emotes like damide1Hi are not available at the moment. However, you can directly use the url of a specific picture with **!kekthis** or **!kekthat**. In this way you can literally transform any picture into braille, PogChamp!<br/>
* *N.B.1*: The emote names are case sensitive! **!kekthis** poggers will return an error, but **!kekthis** POGGERS will work.<br/>
* *N.B.2*: Kekbot braille art will not be properly displayed on mobile, or more generally on a not-standard Twitch chat interface. 
* *N.B.3*: Some of the picture-to-braille transformations sucks (have you tried with BibleThump?). 

### Examples

Command | Result
------------ | -------------
**!kekthis** KappaHD (valid for all the [BTTV emotes](https://betterttv.com/emotes/top) and [Global Twitch emotes](https://twitchemotes.com)) <br/><br>**!kekthis** https://static-cdn.jtvnw.net/emoticons/v2/115847/default/light/2.0 (valid for Twitch channel-specific emotes, or literally any other picture) | <img src="https://github.com/RiccardoBarb/Kekbot/blob/master/examples/Kappa.png" alt="Kappa" width="300"> 
**!kekthat** KappaHD (valid for all the [BTTV emotes](https://betterttv.com/emotes/top) and [Global Twitch emotes](https://twitchemotes.com)) <br/><br>**!kekthat** https://static-cdn.jtvnw.net/emoticons/v2/115847/default/light/2.0 (valid for Twitch channel-specific emotes, or literally any other picture)| <img src="https://github.com/RiccardoBarb/Kekbot/blob/master/examples/Kappa_neg.png" alt="Kappa_neg" width="300">

## How AI generated copypastas work

Kekbot can generate more than 2000 unique "fake" copypastas. This experimental feature is based on the open source project [textgenrnn](https://github.com/minimaxir/textgenrnn) which allows to train a Recurrent Neural Network on a specific dataset and generate texts that mimics the learned style. [The dataset](https://github.com/RiccardoBarb/Kekbot/blob/master/Data/copypasta/pasta_dataset.csv) was scraped from the "Popular" section of [Twitch Quotes](https://www.twitchquotes.com/copypastas?popular=true).
To spam one of the "fake" copypastas in chat just type **!kekpasta**.

*More details on the RNN architechture trained on the copypastas coming soon*

### Commands

* **!kekthis** + emote name (case sensitive!) **or** image url: it converts the pixels with high luminance into braille characters and types the result in chat.
* **!kekthat** + emote name (case sensitive!) **or** image url: it works like **!kekthis** but only pixels with low luminance will be converted into braille. 
* **!kekwho**: Kekbot describes itself and encourage the use of **!kekhow**
* **!kekhow**: Kekbot returns channel-specific messages.
* **!kekpasta**: Kekbot spam an [AI generated copypasta](https://github.com/RiccardoBarb/Kekbot/blob/master/Data/copypasta/deep_fake_pasta.csv)
