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

# sentences = ["Peter pick up the green hammer.",
#              "Peter take the brown box",
#              "Peter got to the golden tree"]

# sentences = ["Justin saw a yellow umbrella.",
#              "Justin give me the yellow umbrella",
#              "My brother and Justin went to the dog.",
#              "The little yellow dog barked at the cat"]


for sentence in sentences:
    text_tagged = utils.stanford_pos_tag(sentence)
    #text_tagged = utils.stanford_named_entity_tag(sentence)

    subjects = []
    verbs = []
    objects = []

    #grammar = "NP: {<DT>?<JJ>*<NN>}"
    grammar = r"""
      NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
      VP: {<VB.*>}
      PP: {<IN><NP>}               # Chunk prepositions followed by NP
      VP: {<VB.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
      CLAUSE: {<NP><VP>}           # Chunk NP, VP
      """

    # grammar = r"""
    #       NP: {<N.*>}          # Chunk sequences of DT, JJ, NN
    #       VP: {<V.*>}               # Chunk prepositions followed by NP
    #       CLAUSE: {<NP><VP>}           # Chunk NP, VP
    #       """

    grammar = """
        Adverb: {<RB>}
        Adject: {<J.*>}
        Subject: {<N.*>}
        Action: {<V.*>} 
        Direction: {<RP>}
        Description: {<Adverb|Adject>}
        SubjectDescription: {<Description>*<Subject>}
        SubjectDescriptions: {<SubjectDescription><CC><SubjectDescription> | <SubjectDescription><,><SubjectDescription> | <SubjectDescription>+}
        ActionDescription: {<Description>*<Action><Description>*<Direction>*}
        ActionDescriptions: {<ActionDescription><CC><ActionDescription> | <ActionDescription><,><ActionDescription> | <ActionDescription>+}
        SubjectActions: {<SubjectDescriptions><.*>*<ActionDescriptions>}
        Target: {<DT>*<SubjectDescriptions>} 
        SubjectActionTarget : {<SubjectAction><.*>*<Target>}
        """

    grammar = """
            Adverb: {<RB>}
            Adject: {<J.*>}
            Subject: {<N.*>}
            Action: {<V.*>} 
            Direction: {<RP>}
            Descriptor: {<Adverb|Adject>}
            Sequencer: {<CC | ,>}
            
            SubjectDescription: {<Descriptor>*<Subject>}
            ActionDescription: {<Descriptor>*<Action><Descriptor>*<Direction>*}
            ActionRelation: {<ActionDescription><TO><DT>*<SubjectDescription> | <ActionDescription><DT><SubjectDescription> | <SubjectDescription><PRP><ActionDescription>}
            
            ActionSummary: {<ActionRelation | ActionDescription>}
            
            SubjectDescriptions: {<SubjectDescription><Sequencer><SubjectDescription> | <SubjectDescription>+}
            
            
            
            SubjectActions: {<SubjectDescriptions><.*>*<ActionDescriptions>}
            
            """
    # ActionSummaries: {(<ActionSummary><Sequencer><ActionSummary>)+ | <ActionSummary>+ }

    grammar = """
                Adverb: {<RB>}
                Adject: {<J.*>}
                Subject: {<N.*>}
                Action: {<V.*>} 
                Direction: {<RP>}
                Descriptor: {<Adverb|Adject>}
                Sequencer: {<CC | ,>}

                SubjectDescription: {<Descriptor>*<Subject>}
                ActionDescription: {<Descriptor>*<Action><Descriptor>*<Direction>*<PRP>*}
                ActionRelation: {<ActionDescription><TO><DT>*<SubjectDescription><Sequencer><ActionDescription> | <ActionDescription><TO><DT>*<SubjectDescription> | <ActionDescription><DT><SubjectDescription>}


                SubjectDescriptions: {<SubjectDescription><Sequencer><SubjectDescription> | <SubjectDescription>+}

                """

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




    for word, tag in text_tagged:
        if tag.startswith("N") and not verbs:
            subjects.append(word)
        elif tag.startswith("V"):
            verbs.append(word)
        elif tag.startswith("N") and verbs:
            objects.append(word)

    grammar_result = cp.parse(text_tagged)

    print sentence
    print text_tagged
    print "Subjects: {}".format(subjects)
    print "Verbs: {}".format(verbs)
    print "Objects: {}".format(objects)

    print "Grammar: {}".format(grammar_result)
    grammar_result.draw()
    print ""



#print nltk.help.upenn_tagset()
