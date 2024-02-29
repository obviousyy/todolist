一个简单的本地的任务表。

1.使用的是mongodb，数据库名为todolist，表名为todolist，文档格式示例如下：

  {
      "_id": ObjectId("65df4aa0e086fedfefdf40a6"),
      "title": "休假日的坏人先生",
      "content": "",
      "priority": NumberInt("4"),
      "cycle": {
          "type": NumberInt("1"),
          "cyclicality": NumberInt("1"),
          "finish_times": NumberInt("8"),
          "total_times": NumberInt("8")
      },
      "begin": ISODate("2024-02-26T01:35:00.000Z"),
      "end": ISODate("2024-03-04T01:35:00.000Z"),
      "is_finish": NumberInt("0"),
      "parent_task": ObjectId("65df4d1be086fedfefdf40bc")
  }

2.双击查看，右键其他功能

3.任务

1）一次性任务

开始和结束时间都能不设，完成了就是完成了。

2）重复任务

时间同上，可以设置需要完成的次数，右键完成一次就完成一次，完成次数达到需要完成的次数则完成。

3）定期任务

不设开始时间默认当天零点或者第二天零点，自动设定结束时间，结束时间为下一个周期的开始时间，到达结束时间自动更新时间并增加需要完成的次数。完成后不再更新

4）阶段任务

不设开始时间默认为当天所在阶段的首日，次数显示连续完成的阶段数，上个阶段未完成则归零。
