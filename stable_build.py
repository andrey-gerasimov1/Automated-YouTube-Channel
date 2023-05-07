import pygame
import os
import glob
import shutil

import praw
from google_images_download import google_images_download

path = os.getcwd()+'/'
pathh = path.replace(os.sep, '/')

location = pathh
dir = "downloads"
path = os.path.join(location,dir)
isdir = os.path.isdir(location)
if isdir == True:
    shutil.rmtree(path)

location = pathh
dir = "downloads"
path = os.path.join(location,dir)
os.mkdir(path)


location = pathh
dir = "audio"
path = os.path.join(location,dir)
isdir = os.path.isdir(location)
if isdir == True:
    shutil.rmtree(path)

location = pathh
dir = "audio"
path = os.path.join(location,dir)
os.mkdir(path)


location = pathh
dir = "formatted_images"
path = os.path.join(location,dir)
isdir = os.path.isdir(location)
if isdir == True:
    shutil.rmtree(path)

location = pathh
dir = "formatted_images"
path = os.path.join(location,dir)
os.mkdir(path)

print(os.getenv("PRAW_CLIENT_ID"))

reddit = praw.Reddit(client_id = os.getenv("PRAW_CLIENT_ID"),
client_secret = os.getenv("PRAW_CLIENT_SECRET"),
username=os.getenv("PRAW_REDDIT_USERNAME"),
password=os.getenv("PRAW_REDDIT_PASSWORD"),
user_agent=os.getenv("PRAW_USER_AGENT"))


titlelist = []
titleauthorlist = []

fullclist = []
fullcalist = []

renamecount = 0

countToImage = []

glbltitlelist = []
glbltitlecount = []

for submission in reddit.subreddit("todayilearned").top(time_filter='day',limit=2):
    if not submission.stickied:

        #adds title and author of post in seperate but in sync lists
        titlelist.append(submission.title)
        titleauthorlist.append(submission.author)

        glbltitlelist.append(submission.title)
        #glbltitlecount.append(len(list(submission.title)))


        titletext = list(submission.title)
        countToImage.append(len(titletext))
        newcharlist = []
        for i in range(len(titletext)):
            charnum = ord(titletext[i])
            if (charnum >= 65 and charnum <= 90) or (charnum >= 97 and charnum <= 122) or charnum == 32:
                newcharlist.append(titletext[i])
            if len(newcharlist) > 100:
                break

        newcharstring = ""
        
        for j in range(len(newcharlist)):
            newcharstring += newcharlist[j]

        #instantiate the class
        response = google_images_download.googleimagesdownload()
        arguments = {"keywords":newcharstring,
                    "limit":1,"print_urls":False}
        paths = response.download(arguments)

        #print complete paths to the downloaded images
        print(paths)

        folderlist = glob.glob('downloads/*')

        folderlist = [e[10:] for e in folderlist]
        print(folderlist)

        frmtcount = format(renamecount,'05d')

        os.rename('downloads/'+str(folderlist[0]),'formatted_images/'+str(frmtcount))

        #curlocation = "C:/Users/jacob/Desktop/imagestest/downloads/"+str(folderlist[0])
        #tarlocation = "C:/Users/jacob/Desktop/imagestest/formatted_images/"

        #shutil.move(curlocation,tarlocation)



        renamecount+=1




        commentslist = []
        commentsauthorlist = []
        if len(submission.comments) > 0:
            commentslist.append(submission.comments[0].body)
            commentsauthorlist.append(submission.comments[0].author)

            if len(submission.comments[0].replies) > 0:
                commentslist.append(submission.comments[0].replies[0].body)
                commentsauthorlist.append(submission.comments[0].replies[0].author)

                #if len(submission.comments[0].replies[0].replies) > 0:
                    #commentslist.append(submission.comments[0].replies[0].replies[0].body)
                    #commentsauthorlist.append(submission.comments[0].replies[0].replies[0].author)
        fullclist.append(commentslist)
        fullcalist.append(commentsauthorlist)
        


#print(len(fullclist))
#print(len(fullcalist))
#print(len(titlelist))
#print(len(titleauthorlist))

location = pathh
dir = "screenshots"
path = os.path.join(location,dir)
isdir = os.path.isdir(location)
if isdir == True:
    shutil.rmtree(path)

location = pathh
dir = "screenshots"
path = os.path.join(location,dir)
os.mkdir(path)


pygame.init()

resW = 1920
resH = 1080

display_surface = pygame.display.set_mode((resW, resH))

pygame.display.set_caption('pygame screenshot taker')

folderlist = glob.glob('formatted_images/*')

folderlist = [e[17:] for e in folderlist]


workingListListList = []

for postcounter in range(len(titlelist)):

    location = pathh+"screenshots/"
    dir = "post" + format(postcounter,'05d')
    path = os.path.join(location,dir)
    isdir = os.path.isdir(location)
    os.mkdir(path)

    bgrColor = [50,50,50]
    display_surface.fill(bgrColor)

    picPosX = 3*(resW/4)
    picPosY = resH/3

    picW = resW/3

    curfolder = pathh+"formatted_images/" + str(folderlist[postcounter]) + "/"
    selimage = os.listdir(curfolder)


    if len(selimage) > 0:
        pic = pygame.image.load("formatted_images/"+str(folderlist[postcounter])+"/"+selimage[0])
        origPicW, origPicH = pic.get_size()
        if origPicW < origPicH:
            imgrtio = picW/origPicH
        else:
            imgrtio = picW/origPicW
        newtpcw = (imgrtio*origPicW)
        newtpch = (imgrtio*origPicH)
        tpcx = (abs(newtpcw - picW))/2
        tpcy = (abs(newtpch - picW))/2
        topicimg = pygame.transform.scale(pic,(newtpcw,newtpch))
        display_surface.blit(topicimg,(picPosX-newtpcw/2,picPosY-newtpch/2))





    def postOutline(postX,postY,postW,postH,authorName,txt,tcount):

        textheight = 0
        fontsize = 0
        fontfile = 'verdana.ttf'

        while textheight < postH:
            font = pygame.font.Font(fontfile, fontsize)
            textheight = renderTextCenteredAt(txt, font, bgrColor, postX, postY, display_surface, postW)
            fontsize+=1
        fontsize-=2

        pygame.draw.rect(display_surface,bgrColor,pygame.Rect(postX,postY,postW,postH))

        font = pygame.font.Font(fontfile, fontsize)
        fontColor = [230,230,230]
        txtchars = list(str(txt))
        charLists = [[]]
        j = 0
        for i in range(len(txtchars)):
            charLists[j].append(txtchars[i])
            if txtchars[i] == ',' or txtchars[i] == '.' or txtchars[i] == ';' or txtchars[i] == ':' or txtchars[i] == '?' or txtchars[i] == '!':
                charLists.append([])
                j+=1
        if charLists[len(charLists)-1] == []:
            charLists.pop()
        

        drawRatio = resW/1920
        vLineX = postX - (30*drawRatio)
        vLineY = postY
        vLineW = 10*drawRatio
        vLineH = postH

        pygame.draw.rect(display_surface,[30,30,30],pygame.Rect(vLineX,vLineY,vLineW,vLineH))

        prfPicSize = 40*drawRatio

        prfPic = pygame.image.load('avdef.png')
        prfPic = pygame.transform.scale(prfPic,(prfPicSize,prfPicSize))

        prfPicX = vLineX + vLineW/2 - prfPicSize/2
        prfPicY = vLineY - prfPicSize/2 - (30*drawRatio)

        display_surface.blit(prfPic,(prfPicX,prfPicY))

        uBtnSize = 20*drawRatio

        uBtn = pygame.image.load('ubtn.png')
        uBtn = pygame.transform.scale(uBtn,(uBtnSize,uBtnSize))

        uBtnX = postX + uBtnSize/2
        uBtnY = postY + postH + uBtnSize/2

        display_surface.blit(uBtn,(uBtnX,uBtnY))

        dBtnSize = 20*drawRatio

        dBtn = pygame.image.load('dbtn.png')
        dBtn = pygame.transform.scale(dBtn,(dBtnSize,dBtnSize))

        dBtnX = postX + dBtnSize/2 + (70*drawRatio)
        dBtnY = postY + postH + dBtnSize/2

        display_surface.blit(dBtn,(dBtnX,dBtnY))


        fontfile = 'verdanai.ttf'
        authorfont = pygame.font.Font(fontfile,18)
        authorW, authorH = authorfont.size(authorName)
        authorX = prfPicX + (60*drawRatio)
        authorY = prfPicY + authorH/2

        author_surface = authorfont.render(authorName, True, [200,200,200])
        display_surface.blit(author_surface, (authorX,authorY))

        #newText = ""
        #directory = str(i)
        #parent_dir = 'C:/Users/jacob/Desktop/imagestest/screenshots'
        #path = os.path.join(parent_dir, directory)
        #os.mkdir(path)

        newText = ""


        location = pathh+"screenshots/post"+format(postcounter,'05d')+"/"
        dir = "folder" + format(tcount,'05d')
        path = os.path.join(location,dir)
        os.mkdir(path)

        os.chdir(pathh+"screenshots/post"+format(postcounter,'05d')+"/folder"+format(tcount,'05d'))


        workingList = []
        for i in range(len(charLists)):
            tempText = ""
            for j in range(len(charLists[i])):
                newText += charLists[i][j]
                tempText += charLists[i][j]
            #tempText = list(tempText)
            #tempText.pop()
            #finText = ""
            #for h in range(len(tempText)):
                #finText += tempText[h]
            #tlen = len(tempText)
            #tempText = tempText[:tlen-1]
            workingList.append(tempText)
            pygame.draw.rect(display_surface,bgrColor,pygame.Rect(postX,postY,postW,postH))
            textheight = renderTextCenteredAt(newText, font, fontColor, postX, postY, display_surface, postW)
            pygame.image.save(display_surface, 'reddit' + format(i,'05d') + '.png')
        os.chdir(r"C:\Users\jacob\Desktop\imagestest")
        return workingList






    def renderTextCenteredAt(text, font, colour, x, y, screen, allowed_width):
        
        words = text.split()

        
        lines = []
        while len(words) > 0:
            
            line_words = []
            while len(words) > 0:
                line_words.append(words.pop(0))
                fw, fh = font.size(' '.join(line_words + words[:1]))
                if fw > allowed_width:
                    break

            
            line = ' '.join(line_words)
            lines.append(line)

        
        y_offset = 0
        for line in lines:
            fw, fh = font.size(line)

            
            tx = x
            ty = y + y_offset

            font_surface = font.render(line, True, colour)
            screen.blit(font_surface, (tx, ty))

            y_offset += fh
        
        return y_offset



    tauthor = str(titleauthorlist[postcounter])
    tbody = str(titlelist[postcounter])

    threadcount = 0

    workingListList = []

    workingListList.append(postOutline(150,150,800,300,tauthor,tbody,threadcount))
    threadcount+=1

    while threadcount <= len(fullclist[postcounter]):
        tauthor = str(fullcalist[postcounter][threadcount-1])
        tbody = str(fullclist[postcounter][threadcount-1])
        if threadcount == 1:
            workingListList.append(postOutline(250,650,1500,150,tauthor,tbody,threadcount))
        if threadcount == 2:
            workingListList.append(postOutline(350,900,1500,150,tauthor,tbody,threadcount))
        threadcount+=1
    
    workingListListList.append(workingListList)

##Getting audio clips and putting it all together##

##VERY IMPORTANT TO KEEP ABOVE AND BELOW SECTIONS SEPERATE##

def renderTextCenteredAt2(text, font, colour, x, y, screen, allowed_width):
        
    words = text.split()

    
    lines = []
    while len(words) > 0:
        
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        
        line = ' '.join(line_words)
        lines.append(line)

    
    y_offset = 0

    ccount = 1
    colours = [[255,255,255],[255,255,168],[131,238,255]]
    
    for line in lines:
        ccount = ccount%3
        colour = colours[ccount]
        fw, fh = font.size(line)

        
        tx = x
        ty = y + y_offset

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))

        y_offset += fh

        ccount+=1
    
    return y_offset

#pygame.init()

resW = 1280
resH = 720

display_surface = pygame.display.set_mode((resW, resH))

pygame.display.set_caption('pygame thumbnail taker')


bgrColor = [50,50,50]
display_surface.fill(bgrColor)


chosenImage = min(countToImage)
minIndex = countToImage.index(chosenImage)
txt = titlelist[minIndex]
txt = txt.upper()

textList = list(txt)
if textList[0]+textList[1]+textList[2] == "TIL":
    textList[0] = '.'
    textList[1] = '.'
    textList[2] = '.'

txt = ""
for t in range(len(textList)):
    txt += textList[t]

fontsize = 0
fontfile = 'GothicAXHand-Regular.otf'


postX = 50
postY = 170
postW = 700
textheight = 0
postH = 450

while textheight < postH:
    font = pygame.font.Font(fontfile, fontsize)
    textheight = renderTextCenteredAt2(txt, font, bgrColor, postX, postY, display_surface, postW)
    fontsize+=1
fontsize-=2

display_surface.fill(bgrColor)

renderTextCenteredAt2(txt, font, [0,0,0], postX, postY, display_surface, postW)

drawRatio = resH/720

uBtnSize = 150*drawRatio

uBtn = pygame.image.load('reddit-logo.png')
uBtn = pygame.transform.scale(uBtn,(uBtnSize,uBtnSize))

display_surface.blit(uBtn,(20,20))

font = pygame.font.Font('verdanai.ttf', 50)

font_surface = font.render("r/TodayILearned", True, [255,255,255])
display_surface.blit(font_surface, (200, 70))


picPosX = 3*(resW/4)
picPosY = resH/2

picW = resW/3



chosenImageFolder = pathh+"formatted_images/"+format(minIndex,'05d')+"/"

folderImageFile = os.listdir(chosenImageFolder)

if len(folderImageFile) > 0:
    pic = pygame.image.load("formatted_images/"+format(minIndex,'05d')+"/"+folderImageFile[0])
    origPicW, origPicH = pic.get_size()
    if origPicW < origPicH:
        imgrtio = picW/origPicH
    else:
        imgrtio = picW/origPicW
    newtpcw = (imgrtio*origPicW)
    newtpch = (imgrtio*origPicH)
    tpcx = (abs(newtpcw - picW))/2
    tpcy = (abs(newtpch - picW))/2
    topicimg = pygame.transform.scale(pic,(newtpcw,newtpch))
    oOffset = 10
    pygame.draw.rect(display_surface,[250,0,0],pygame.Rect(picPosX-newtpcw/2-oOffset,picPosY-newtpch/2-oOffset,newtpcw+oOffset*2,newtpch+oOffset*2))
    display_surface.blit(topicimg,(picPosX-newtpcw/2,picPosY-newtpch/2))

arrowPic = pygame.image.load("redArrow.png")
arrowPic = pygame.transform.scale(arrowPic,(400,200))
arrowFlipped = pygame.transform.flip(arrowPic,False,True)
display_surface.blit(arrowFlipped,(450,500))

pygame.image.save(display_surface, 'video_thumbnail.png')




from moviepy.editor import *

"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='C:/Users/jacob/Downloads/pythonyoutube.json'


from google.cloud import texttospeech


# Instantiates a client
client = texttospeech.TextToSpeechClient()

pathsLists = []

for j in range(len(workingListListList)):

    location = pathh+"audio/"
    dir = format(j,'05d')
    path1 = os.path.join(location,dir)
    os.mkdir(path1)

    pathsLists.append([])

    for h in range(len(workingListListList[j])):

        location = path1
        dir = format(h,'05d')
        path2 = os.path.join(location,dir)
        os.mkdir(path2)

        pathsLists[j].append([])

        for p in range(len(workingListListList[j][h])):

            outputfile = 'output'+format(p,'05d')+'.mp3'
            #outputList.append(outputfile)

            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=workingListListList[j][h][p])

            # Build the voice request, select the language code ("en-US") and the ssml
            # voice gender ("neutral")
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )

            # Select the type of audio file you want returned
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            

            # The response's audio_content is binary.
            with open(outputfile, "wb") as out:
                # Write the response to the output file.
                out.write(response.audio_content)
                print('Audio content written to corresponding output file')
            
            shutil.move(outputfile,pathh+'audio/'+format(j,'05d')+'/'+format(h,'05d')+'/'+outputfile)
            pathsLists[j][h].append(pathh+'audio/'+format(j,'05d')+'/'+format(h,'05d')+'/'+outputfile)



# for j in range(len(workingListListList)):
#     newSpeech = []
#     newSpeech.append(workingListListList[j])
#     for i in range(len(fullclist[j])):
#         newSpeech.append(fullclist[j][i])
#     eachSpeech.append(newSpeech)

# print(fullclist)
# print(eachSpeech)

# mainOutList = []

# for k in range(len(eachSpeech)):

#     location = "C:/Users/jacob/Desktop/imagestest/audio/"
#     dir = format(k,'05d')
#     path = os.path.join(location,dir)
#     os.mkdir(path)

#     xmpleList = eachSpeech[k]
#     outputList = []

#     for i in range(len(xmpleList)):
#         outputfile = 'output'+format(i,'05d')+'.mp3'
#         outputList.append('audio/'+str(dir)+"/"+outputfile)
#         # Set the text input to be synthesized
#         synthesis_input = texttospeech.SynthesisInput(text=str(xmpleList[i]))

#         # Build the voice request, select the language code ("en-US") and the ssml
#         # voice gender ("neutral")
#         voice = texttospeech.VoiceSelectionParams(
#             language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
#         )

#         # Select the type of audio file you want returned
#         audio_config = texttospeech.AudioConfig(
#             audio_encoding=texttospeech.AudioEncoding.MP3
#         )

#         # Perform the text-to-speech request on the text input with the selected
#         # voice parameters and audio file type
#         response = client.synthesize_speech(
#             input=synthesis_input, voice=voice, audio_config=audio_config
#         )

#         # The response's audio_content is binary.
#         with open(outputfile, "wb") as out:
#             # Write the response to the output file.
#             out.write(response.audio_content)
#             print('Audio content written to corresponding output file')
        
#         os.rename(outputfile,'audio/'+str(dir)+"/"+outputfile)
    
#     mainOutList.append(outputList)
        





curfolder = pathh+"screenshots/"
selimage = os.listdir(curfolder)

totalClips = []

transitionVideo = VideoFileClip('redditTransitionVideo.mp4')

for h in range(len(selimage)):
    nextlist = os.listdir(curfolder+selimage[h]+'/')


    colctClips = []

    for p in range(len(nextlist)):

        thirdlist = os.listdir(curfolder+selimage[h]+'/'+nextlist[p]+'/')

        senClips = []

        for y in range(len(thirdlist)):
            
            
            fourthlist = 'screenshots/'+selimage[h]+'/'+nextlist[p]+'/'+thirdlist[y]
            print("fourthlist: " +str(fourthlist))
            print("thirdlist: " +str(thirdlist))
            print("value of y: " + str(y))
            print("pathslists h p: "+ str(pathsLists[h][p]))
            
            utFile = AudioFileClip(pathsLists[h][p][y])
            workClip = ImageClip(fourthlist)
            workClip = workClip.set_audio(utFile)
            workClip = workClip.set_duration(utFile.duration)
            workClip.fps = 5
            senClips.append(workClip)
        senTog = concatenate_videoclips(senClips,method="compose")
        colctClips.append(senTog)
        #colctClips.append(senClips)
    colctTog = concatenate_videoclips(colctClips,method="compose")
    totalClips.append(colctTog)
    totalClips.append(transitionVideo)

finalVideo = concatenate_videoclips(totalClips,method="compose")
bgrMusic = AudioFileClip('redditBackgroundMusic.mp3')
bgrMusic = bgrMusic.set_duration(finalVideo.duration)
bgrMusic = bgrMusic.volumex(0.5)

musicAndSpeech = CompositeAudioClip([finalVideo.audio,bgrMusic])

finalVideo.audio = musicAndSpeech

finalVideo.write_videofile("somevideo.mp4",fps=5)


##youtube execution of command

chosenUploadTitle = min(glbltitlelist, key=len)
chosenUploadList = list(str(chosenUploadTitle))
chosenUploadList.pop(0)
chosenUploadList.pop(0)
chosenUploadList.pop(0)
chosenUploadList.pop(0)
chosenFinalTitle=""
for i in range(len(chosenUploadList)):
    chosenFinalTitle+=chosenUploadList[i]

filename = 'somevideo.mp4'
print(chosenUploadTitle)
title = chosenFinalTitle+'...' + ' | Best Of r/TodayILearned'
print(title)
description = "Like and Subscribe if you enjoyed this video!"
tags = "reddit,todayilearned,educational,funny,entertainment,compilation"
visibility = "public"
print("Starting video upload...")

filecommand = '--file="C:/Users/jacob/Desktop/imagestest/'+str(filename)+'"'
titlecommand = '--title="'+title+'"'

titlecommand = '--title="'+"Let's Goooo!"+'"'

descriptioncommand = '--description="'+str(description)+'"'
keywordscommand = '--keywords="'+str(tags)+'"'
visibilitycommand = '--privacyStatus="'+str(visibility)+'"'
print('py upload_video.py '+filecommand+' '+titlecommand+' '+descriptioncommand+' '+keywordscommand+' '+'--category="22" '+visibilitycommand)

os.system('py upload_video.py '+filecommand+' '+titlecommand+' '+descriptioncommand+' '+keywordscommand+' '+'--category="22" '+visibilitycommand)











# while True:

#     for event in pygame.event.get():

#         if event.type == pygame.QUIT:
 
#             pygame.quit()
 
#             quit()
 
#         pygame.display.update()
