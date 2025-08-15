import asyncio
from ollama_utils import ollama_client
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console

async def main():
    class_assistant = AssistantAgent(
        name="class_assistant",
        model_client=ollama_client,
        system_message="""
        You are a class assistant. Your role is to coordinate the process of creating course content:

        - Summarizer: Responsible for generating a concise summary of the provided material.
        - Question Generator: Responsible for creating questions based on the Summarizer.

        Always submit your plan first, then hand it off to the appropriate agent. 
        You may hand off to only one agent at a time. 
        Always use TERMINATE(block letter) once the summarizer and question_generator return back to you,
        stop to assign work to them.
        """
    )
    
    summarizer = AssistantAgent(
        name="summarizer",
        model_client=ollama_client,
        system_message="""
        You are an expert at understanding course content, 
        merging the transcript with the course outline into a concise 
        and complete summary. Once the summary is complete, it must be 
        handed back to the class_assistant Coordinator."""
    )

    question_generator = AssistantAgent(
        name = "question_generator",
        model_client = ollama_client,
        system_message = """
        You are a question generation expert skilled at 
        creating targeted course questions based on self-organized notes and 
        distilled key points.Once the questions are complete, it must be handed 
        back to the class_assistant Coordinator."""
    )

    # Data
    course_transcript = """
    那接下來我們就來講二三數要怎麼樣插入一個新的node 那如果假設你今天是一個null tree 那你就把東西放進去 這沒有什麼為什麼 因為假設它本來就是一個空數 你東西放進去就放到root的地方嘛 所以我就插入一個二節點 二節點是什麼 大家再想一下 二節點指的是它有兩個branch 裡面可以放一個key值 所以你如果有一個新的東西要放進去 那就放進去啊 那接下來呢 第二種case是什麼 我要插入一個節點到一個二節點的葉子上面 我要插入一個東西到二節點的葉子上面去 那如果我今天要放到一個二節點的葉子 大家還記得嗎 我們在二三數裡面 每一個的node只有兩種嘛 要嘛就是二節點 要嘛就是三節點 所以代表二節點上面如果要再多放一個key值 就讓它變成三節點 所以好像也沒有什麼問題 例如說像這邊 我要把一個東西像3 我要把它插進去 這時候3呢 從上面進來之後 3比8小 比4小 所以我要放到那個node裡面 那個node現在是一個二節點 因為它裡面只有一個key值兩個branch 它是一個1嘛 只有一個1 所以我就把3丟進去 所以放進去就沒問題 懂嗎 那如果我插進去的是0 0比8小 比4小 比1小 所以假設我插進去的是0 那個node就會變成01 就會變成01 我寫錯了 01啦 因為原本是1嘛 好 那接下來第二種情況 假設我要插進的節點是一個三節點的葉子 你就不能說 老師三節點 那我們就讓它變成四節點 沒有 它是二三數 所以最多最多就只能有 放兩個東西 三個branch 所以例如說 我們現在要把東西插進去 這時候我們就會來選一下 它的排序的內容 把中間的往上做 好 例如說我現在要插進來是5 5比8小 比4來的大 所以我的5要放在這邊 所以5要丟進去的話 應該是什麼 會變567嘛 所以這時候我們會做什麼 我們會把567裡面的6往上移 我們會把6往上移 那這時候呢 6就往上移 6往上移之後 這邊就會變成4跟6 那4跟6就是一個什麼 三節點 所以這時候 4跟6就會變成三個branch 所以就會變成三條線嘛 所以這一條線沒有動 但是4跟6的中間有一條線 就會堆到5 另外一條線就會去6跟 就會到7 所以這時候5放進去 這邊567 6往上提會變成4跟6 所以這邊一個5一個7 就會變成長這樣子 這就是在這個裡面 我覺得比較複雜的部分 就是當你放進去的時候 可能會是這樣的情況 你就必須要做這件事情 所以這時候5跟7 就會被你拆開來 為什麼 因為上面的那個東西 變成4跟6 變成一個三節點 那三節點就會有三個branch 所以你要讓每個branch都有東西 所以原本裡面 假設你把6往上提 你以為是5跟7 千萬不要寫成這樣這樣喔 考試的時候超常看到這樣子的 其實我還蠻喜歡改 期末的時候改各位的Btree 因為你們的Btree都會寫得 不知道在寫什麼東西 你們就很多人就會寫成像這樣 就我把6往上提 然後我根本不管這裡面 其實是應該要有三個branch 所以這個地方就會錯 所以不能這樣子 你要記得 如果假設它變成一個三節點 它就會有三個branch 那你要符合原本5跟7 所以5跟7就要拆掉 變成5跟7 就要長成像這樣子 那接下來假設我要插進的是11 那11要放哪裡呢 11比8大比12小 所以我要插在這邊 來大家看這邊 所以我要丟進去的時候 會發生什麼事情 就放不進去啊 因為9 10 11啊 我又不能放三個key字 所以9 10 11誰要往上提 就10嘛對不對 那10往上提之後你會發現 上面也不可以放啊 上面有誰 10 12跟14 所以就要把中間的再往上提 所以你可以看到 當我要放進11的時候 底下的滿了 就往上提一個10 10 12 14的12就往上提 所以這邊會變成8跟12 那一樣8跟12 剛剛原本的底下是10跟14嘛 10跟14就分開來 10的兩邊就是9跟11有沒有 因為這邊本來是9跟11嗎 9跟11就被你分開來 那這邊的13 15就找9 所以當你放進去發現滿了 你就會開始往上堆 然後往上堆上面滿了 就再往上堆 不要忘記只要東西一增加 它的branch就會增加 東西變少 branch變少 東西還是要拆分 所以一定要記得把東西拆開來 一定要記得把東西拆開來 不要就是丟進去 東西又還不是合併在一起 這樣會很奇怪 每一個東西的branch 假設有兩個key字 就是會有三個branch 假設它只有一個key字 就是會有兩個branch 接下來我再丟 例如說在那邊丟個2 2比8小比4小 丟到這邊 一樣嘛 123不就滿了嗎 把2往上提 2往上提之後246 4又滿啦 4就往上提 482又滿啦 8就往上提 所以再往上提就會變成長這樣子 所以當東西拆得越多的時候 23數就會開始 你知道 深度就會增加 那深度增加之後 對我們其實是比較不利的 但是沒辦法 我們東西就要放這麼多 所以它就會長成像這個樣子 好 所以我們再來看 來 例如說 我有寫啦 我們這邊就不讓大家做 但是你回家之後 自己要做看看 來我們來丟看看 首先60 60要丟到哪裡去啊 60比45來得大 比70小 所以60丟在這邊 OK嗎 可不可以放進去 可以 不會滿喔 所以60放進去在這邊 OK吧 將近90 90比45來得大 比70來得大 會不會滿 會 85跟90 把中間的85往上提 這邊就變成70跟85 70跟85會不會滿 不會 所以70 85在一起的時候 中間有三個branch 所以這邊原本裡面有80 90 就把它們拆開來 可以齁 接下來 這就剛剛的 這就不管 這一頁其實都在說明 我們剛剛講的事情 接下來再加誰 加55 55比45來得大 比70來得小 是不是要加這 對吧 可是55加進去 東西就滿了 所以55要往上提對不對 55一往上提 裡面是不是又滿了 所以70就往上提 那70往上提 上面會不會滿 不會嘛 上面本來就可以放到兩個嘛 所以上去之後 這邊就變成 45 70 然後85跟80 85這樣 有問題嗎 就是55往上嘛 55往上 70往下 這邊就有三個branch 然後 那因為剛剛 這個中間的70往上 所以這邊就把東西又拆開來 一拆開來 這邊就分開來了 那接下來呢 另外這個 假設我加進15 15比45來得小 比30來得小 是不是加這邊 15加進去之後會滿 所以15就往上提 15一往上提 這邊就會變成15跟30 15跟30就要有三條線 中間那條線沒有 所以20就去中間那條線 所以就會變成這樣子 這樣回去會做 所以這邊就是 簡單的事情 那接下來呢 我們再加25 25加進去 25會比這邊來得小 然後接在15跟30的中間 所以25加進去 會不會有什麼問題 沒有問題 25就放在這邊裡面嘛 對不對 就是加進去就長這樣子 因為那就沒有滿 因為只有一個東西 加一個有什麼關係 好 接下來加17呢 17進來比45來得小 接在15跟30中間走下來 是不是放這邊 所以17要放這邊對不對 會不會滿 會 那把誰往上提 把20往上提 因為17 20 25嘛 20往上提 20往上提之後是不是滿了 滿了20又再往上提 20 45 70 是不是再把45往上提 所以就最上面是45 45就把剛剛的20 70分開來 以此類推後面的東西也一起分開來 所以這時候加進去
    """

    course_outline = """
    Chapter 18 B-Trees
    """

    step1_prompt = f"""
    Please integrate the following transcript and the course outline and write a summary and questions in English:
    transcript:
    {course_transcript}
    course outline：
    {course_outline}
    """
    
    text_termination = TextMentionTermination("TERMINATE")
    termination = text_termination
    
    research_team = SelectorGroupChat(
        participants=[class_assistant, summarizer, question_generator],
        model_client = ollama_client,
        termination_condition=termination
    )
    await Console(research_team.run_stream(task=step1_prompt))
    
    await ollama_client.close()

if __name__ == "__main__":
    asyncio.run(main())
