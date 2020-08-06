from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.index import create_in, open_dir
# from whoosh.query import *
# from whoosh.qparser import *
from jieba.analyse import ChineseAnalyzer
import pymongo
from pymongo.collection import Collection
import settings



class IndexBuilder:
    def __init__(self):
        self.mongoClient = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
        #self.db = self.mongoClient[settings.MONGODB_DBNAME][settings.MONGODB_SHEETNAME]
        self.db = pymongo.database.Database(self.mongoClient, settings.MONGODB_DBNAME)
        self.pagesCollection = Collection(self.db, settings.MONGODB_SHEETNAME)
        # collection = self.db["url"]
        #
        # for url in collection.distinct('url'):  # 使用distinct方法，获取每一个独特的元素列表
        #     num = collection.count({"url": url})  # 统计每一个元素的数量
        #     for i in range(1, num):  # 根据每一个元素的数量进行删除操作，当前元素只有一个就不再删除
        #         print('delete %s %d times ' % (url, i))
        #         # 注意后面的参数， 很奇怪，在mongo命令行下，它为1时，是删除一个元素，这里却是为0时删除一个
        #         collection.remove({"url": url}, 0)
        #     for i in collection.find({"url": url}):  # 打印当前所有元素
        #         print(i)
        # print(collection.distinct('url'))   # 再次打印一遍所要去重的元素)

    def build_index(self):
        analyzer = ChineseAnalyzer()

        # 创建索引模板
        schema = Schema(
            Id=ID(stored=True),
            title=TEXT(stored=True, analyzer=analyzer),
            url=ID(stored=True),
            reply=NUMERIC(stored=True, sortable=True),
            author=TEXT(stored=True),
            last_reply_time=TEXT(stored=True),
            introduction=TEXT(stored=True, analyzer=analyzer),
        )

        # 索引文件相关
        import os.path
        if not os.path.exists('index'):
            os.mkdir('index')
            ix = create_in('index', schema)
            print('未发现索引文件,已构建.')
        else:
            ix = open_dir('index')
            print('发现索引文件并载入....')

        # 索引构建
        writer = ix.writer()
        indexed_amount = 0
        total_amount = self.pagesCollection.count_documents({})
        false_amount = self.pagesCollection.count_documents({'indexed': 'False'})
        print(false_amount, '/', total_amount)
        while True:
            try:
                row = self.pagesCollection.find_one({'indexed': 'False'})
                if row is None:
                    # all indexed is 'True' 所有条目已经处理
                    writer.commit()
                    print('所有条目索引处理完毕.')
                    break
                else:
                    # get new row 获取了新的条目

                    writer.add_document(
                        Id=str(row['_id']),
                        title=row['title'],
                        url=row['url'],
                        reply=int(row['reply']),
                        author=row['author'],
                        last_reply_time=row['last_reply_time'],
                        introduction=row['introduction'],
                    )

                    # the end
                    self.pagesCollection.update_one({'_id': row['_id']}, {'$set': {'indexed': 'True'}})
                    writer.commit()  # 每次构建提交一次
                    writer = ix.writer()  # 然后重新打开
                    indexed_amount += 1
                    print(indexed_amount, '/', false_amount, '/', total_amount)
            except:
                print(row['_id'], '异常.')
                print('已处理', indexed_amount, '/', total_amount, '项.')
                break


# --------此段代码用以在数据库中缺少indexed字段时补充插入indexed字段并初始化为false--------
#         host = settings.MONGODB_HOST
#         port = settings.MONGODB_PORT
#         dbname = settings.MONGODB_DBNAME
#         sheetname = settings.MONGODB_SHEETNAME
#         client = pymongo.MongoClient(host=host, port=port)
#         mydb = client[dbname]
#         post = mydb[sheetname]
#         post.update({}, {'$set':{'indexed':'False'}}, upsert=False, multi=True)   # 增加indexed项并初始化为False
#         post.update({'indexed': 'True'}, {'$set':{'indexed':'False'}})
# --------------------------------------------------------------------------------------

if __name__ == '__main__':
    id = IndexBuilder()
    id.build_index()
