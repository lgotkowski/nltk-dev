import nltk
import utils

actions = {"walk": ["walk", "go", "run", "move"],
           "grab": ["grab", "take", "pickup", "drag", "bring"],
           "look": ["look", "view", "see"],
           "state": ["be"]}

emotions = ["happy", "angry", "sad"]

directions = ["up", "down", "left", "right"]

speed = ["fast", "slow", "normal"]

locations = ["onto", "under", "next to"]

sentences = ["Clever Peter and stupid Justin walk to the biggest window.",
             "Amazing Peter and clever Justin, slowly stand up and walk quickly to the biggest tree.",
             "Amazing Peter and clever Justin, slowly stand up, find the biggest tree and go there quickly.",
             "Peter and Justin can you walk to the window.",
             "Peter and Justin can you quickly walk to the blue window.",
             "Peter and Justin can you walk quickly to the window.",
             "Peter please go to the old tree.",
             "Peter, Justin, please go to the sport car.",
             "Peter, Justin, please go to Phine.",
             "Peter, Justin, please go away from Phine.",
             "Peter and Justin, you two have to jump to the left door.",
             "Peter and Justin, you two have to jump to Phine.",
             "Peter pick up the green hammer.",
             "Peter take the brown box",
             "Peter got to the golden tree"]

sentences = ["Happy Fussel, find the big blue tree and take it",
             "Angry Fussel, find the boy and the girl and draw them",
             "Blue Justin look for the boy and draw him",
             "Holy Phine find the tree and go there",
             "Holy Phine find the tree and go there and wave your hand"]



for sentence in sentences:
    text_tagged = utils.stanford_pos_tag(sentence)

    grammar = """
                Adv: {<RB>}
                Adj: {<J.*>}
                Subject: {<N.*>}
                Action: {<V.*>}
                Direction: {<RP>}
                Prep: {<PRP.*>}
                Desc: {<Adv|Adj>+}
                Seq: {<CC|,>}
                Rel: {<IN|TO>}
                
                ActDesc: {<Desc>*<Action><Desc>*}
                SubDesc: {<DT>*<Desc>*<Subject>}
                
                ActPrep: {<ActDesc><Prep>}
                
                SubDescList: {(<DT>*<SubDesc><Seq><DT>*<SubDesc>)+ | <DT>*<SubDesc>+}
                
                ActRel: {<ActDesc><Rel>*<SubDescList><Seq><ActPrep> | <ActDesc|ActPrep><Rel>*<SubDescList>}
                """

    for i in range(len(text_tagged)):
        word, tag = text_tagged[i]
        if word == "there":
            text_tagged[i] = (word, "PRP")


    cp = nltk.RegexpParser(grammar)


    grammar_result = cp.parse(text_tagged)

    print sentence
    print text_tagged
    print "Grammar: {}".format(grammar_result)
    grammar_result.draw()
    print ""



#print nltk.help.upenn_tagset()


# TODO: find the action verbs and match them to the possible actions of the character. (find neares word?)
# -> same for subjects

# TODO: format the grammar_result in a nicer way to be more intuetive.