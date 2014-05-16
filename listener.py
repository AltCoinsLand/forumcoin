import networking, custom, tools, leveldb, blockchain
#Sometimes peers ask us for information or push new transactions or blocks to
#us. This file explains how we respond.
def main(dic, DB):
    
    def security_check(dic):
        if 'version' not in dic or dic['version']!=custom.version:
            return {'bool':False, 'error':'version'}
        else:
            #we could add security freatures here.
            return {'bool':True, 'newdic':dic}
            
    def blockCount(dic, DB):
        length=DB['length']
        if length>=0:
            return {'length':length, 'diffLength':DB['diffLength']}
        else:
            return {'length':-1, 'recentHash':0, 'diffLength':'0'}
            
    def rangeRequest(dic, DB):
        ran=dic['range']
        out=[]
        counter=0
        while len(tools.package(out))<custom.max_download and ran[0]+counter<=ran[1]:
            block=blockchain.db_get(ran[0]+counter, DB)
            if 'length' in block:
                out.append(block)
            counter+=1
        return out
        
    def txs(dic, DB): return DB['txs']
    
    def pushtx(dic, DB): 
        DB['suggested_txs'].append(dic['tx'])
        return 'success'
        
    def pushblock(dic, DB):
        DB['suggested_blocks'].append(dic['block'])
        return 'success'
        
    funcs={'blockCount':blockCount, 'rangeRequest':rangeRequest, 
           'txs':txs, 'pushtx':pushtx, 'pushblock':pushblock}
    if dic['type'] not in funcs.keys():
        return str(dic['type'])+' is not in the api'
    try:
        check=security_check(dic)
        if not check['bool']:
            return check
        return funcs[dic['type']](check['newdic'], DB)
    except:
        pass

def server(DB): return networking.serve_forever(main, custom.listen_port, DB)
