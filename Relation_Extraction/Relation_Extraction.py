import pyltp
#Loading environment
segmentor, postagger, parser = Segmentor(), Postagger(), Parser()
segmentor.load_with_lexicon( path + 'ltp_model/cws.model', path + "dictionary_full.txt")
postagger.load(path + 'ltp_model/pos.model')
parser.load(path + 'ltp_model/parser.model')

def relation_extraction(text):
    for sen in text.split('，'):
        print('Extract relations:')
        words = segmentor.segment(sen)
        postags = postagger.postag(words)
        arcs = parser.parse(words, postags)
        ws = list(words)
        
        parsing = {}
        features = []
        core = []
        core_verb = {'为','设有','有','包括'}
        for vid, pos in enumerate(postags):
            if pos in {'v'}:
                if (arcs[vid].relation in {'HED','COO'})  or (arcs[vid].head-1 in core) or (ws[vid] in core_verb): #核心谓语
                    core.append(vid)
                    verb = [(ws[vid], vid)]
                    sub, sub_id = [], []
                    obj, obj_id = [], []
                    
                    #谓语的主语&谓语&状语
                    for nid, n_arc in enumerate(arcs):
                        if n_arc.relation in {'SBV'}: 
                            if (n_arc.head-1 == vid):
                                sub.append((ws[nid],nid))
                                sub_id.append(nid)
                        elif n_arc.relation in {'VOB','POB','CMP','COO'}: 
                            if (n_arc.head-1 == vid):
                                obj.append((ws[nid],nid))
                                obj_id.append(nid)
                        elif n_arc.relation in {'ADV'}: 
                            if (n_arc.head-1 == vid):
                                verb.append((ws[nid],nid))
                                
                    
                    #谓语的主语的定语等            
                    if len(sub_id) != 0:
                        new_add, cache = 1, []
                        while new_add != 0:
                            new_add = 0
                            for nid, n_arc in enumerate(arcs):
                                if nid not in cache:
                                    if n_arc.relation in {'VOB','SBV','ADV','LAD','RAD','ATT','COO','POB'}: 
                                        if n_arc.head-1 in sub_id:
                                            #print(nid, ws[nid])
                                            cache.append(nid)
                                            sub.append((ws[nid],nid))
                                            sub_id.append(nid)
                                            new_add = 1        
                    
                    #谓语的宾语的定语等            
                    if len(obj_id) != 0:
                        new_add, cache = 1, []
                        while new_add != 0:
                            new_add = 0
                            for nid, n_arc in enumerate(arcs):
                                if nid not in cache:
                                    if n_arc.relation in {'VOB','SBV','ADV','LAD','RAD','ATT','COO','POB'}: 
                                        if n_arc.head-1 in obj_id:
                                            #print(nid, ws[nid])
                                            cache.append(nid)
                                            obj.append((ws[nid],nid))
                                            obj_id.append(nid)
                                            new_add = 1


                    sub = [i[0] for i in sorted(list(set(sub)), key =lambda x:x[1])]
                    verb = [i[0] for i in sorted(list(set(verb)), key =lambda x:x[1])]
                    obj = [i[0] for i in sorted(list(set(obj)), key =lambda x:x[1])]
                    print('_'.join(sub),'/', '_'.join(verb), '/', '_'.join(obj))
        
    return segs

