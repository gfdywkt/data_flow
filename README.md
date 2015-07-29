# data_flow
招中标数据判重流程

1. calc_words.py 统计每个单词在当前桶（每100000个标书一个“桶”）中出现次数
2. sum_all_words.py 计算每个单词在所有招中标数据中出现次数
3. tf-idf.py 计算每篇招中标信息中，每个单词的tf-idf值，并取tf-idf前15的单词作为核心词保存
4. key_words_sort.py 把文章的关键词及其权重按关键词字典序排序
5. md5.py 把文章的关键词和权重全部拼成一个字符串，再映射成一个md5串
6. find_repeat.py md5串相同的文章视为重复
