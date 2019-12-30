import csv
import jieba
from snownlp import SnowNLP

def Load():
    with open("諮商輔導中心.csv","r",encoding="utf-8") as csvfile:
        Data_List = csv.reader(csvfile, delimiter=',')
        
        Title = []
        
        for i in Data_List:
            #print(i)
            Title.append(i[2])
    return Title

def Jieba_Analysis(Title):
    jieba.load_userdict('dict.txt.big.txt')
    segment = []

    for i in Title[1:]:
            segment.append(list(jieba.cut(i)))

    #print(segment)

    #心情強度
    Mood = []
    segment_ordered = []
    temp = []

    for i in segment:

        for j in i:
            temp.append((abs(SnowNLP(j).sentiments-0.5),j))
        Mood.append(temp)
        temp = []
    # sort 心情強度 刪除過低的
    for i,ele in enumerate(Mood):
        ele.sort(reverse=True)
        ele = ele[:2]
        #print(ele)
        segment_ordered.append([])
        for item in ele:
            segment_ordered[i].append(item[1])
        
    #print(segment_ordered)
    return segment_ordered

#不知道有沒有用
def Remove_Sapce(Key_List):
    Key_List = Key_List[0:-2]
    if Key_List[-1] == " ":
        Key_List = Remove_Sapce(Key_List)
    return Key_List

def WriteNewCsv(segment_ordered):
    with open("諮商輔導中心8787.csv","w",newline='',encoding='utf-8') as csvFile:
        with open("諮商輔導中心.csv","r",encoding="utf-8") as csvfile:
            Data_List = csv.reader(csvfile, delimiter=',')
            writer = csv.writer(csvFile)
            Combine_keywords = ""
            Key_List = []

            for i in (segment_ordered):
                for j,ele in enumerate(i):
                    if j != len(ele):
                        Combine_keywords += ele + " "
                    else:
                        Combine_keywords += ele

                Key_List.append(Combine_keywords)
                Combine_keywords = ""
                
            #不知道有沒有用
            if Key_List[-1] == " ":
                Key_List = Remove_Sapce(Key_List)
                
            Key_List.insert(0, "關鍵詞")
            
            for i,ele in enumerate(Data_List):
                writer.writerow([ele[0], ele[1], ele[2], ele[3], ele[4], Key_List[i]])

Title = Load()
segment_ordered = Jieba_Analysis(Title)
WriteNewCsv(segment_ordered)