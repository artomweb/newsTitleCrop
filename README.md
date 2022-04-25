## work-in-progress

# News title cropper

A common thing seen in video essays and documentaries, is a clip/animation showing many news articles, centered around the specific word of interest. This is usually done manually in video editing software, where the editor takes many screenshots of news articles and meticulously aligns them to generate the video.

![Vice Metaverse](media/Vox-Metaverse.gif)

A clip from a [Vice news video](https://www.youtube.com/watch?v=bolyiGMcjBs&t=158s&ab_channel=VICENews)

Currently only supports BBC News

## Use:

    python main.py [-h] word numPages

## Example

    python main.py metaverse 1

## Results:

![results](media/Omicron.gif)

## Result with slow zoom:

![results](media/OmicronZoom.gif)

## Ukraine result:

![results](media/Ukraine.gif)

## Result from the Daily Mail:

![results](media/Omicron-DM.gif)

# To-do:

- Add support for the Daily Mail and other news sources and
- Allow words to be found even if surrounded by punctuation, and crop accordingly
