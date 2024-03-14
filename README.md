# 一个简单的本地的任务表。

## 0.只下载dist/main，双击todolist1.exe就可以启动。

是用pyinstall打包的，按[csdn教程](https://blog.csdn.net/qq_62689586/article/details/135143312)创建虚拟环境名`todo1`并安装依赖包，下载整个项目双击`make.bat`可以生成exe文件，也可以设置任一环境名，只需修改`make.bat`中的环境名。

## 1.数据库

使用的是mongodb，数据库名为todolist，表名为todolist，默认是自动连接本地数据库且无账号密码，自己建数据库和表。
文档格式示例如下：（建议使用软件内操作不要自己更改数据库内的数据）

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
        "parent_task": ObjectId("65df4d1be086fedfefdf40bc"),
        "expend": NumberInt("0")
    }

    {
        "_id": ObjectId("65df49f3e086fedfefdf40a1"),
        "title": "小说",
        "content": "",
        "priority": NumberInt("1"),
        "cycle": {
            "type": NumberInt("-1")
        },
        "is_finish": NumberInt("-1"),
        "subtask": [
            ObjectId("65df49ffe086fedfefdf40a2"),
            ObjectId("65df4a11e086fedfefdf40a3"),
            ObjectId("65ee5a2f2a9117d76dc1cf80")
        ],
        "expend": NumberInt("-1")
    }

## 2.双击查看，右键其他功能

### 0）新建任务

右键self新建没有父任务的任务

### 1）一次性任务

可以添加子任务，其余类型均不能设置子任务。

可以设置自动展开或手动展开子节点，手动展开即与上一次关闭时的展开状态相同，自动展开则如果有未完成的子任务或孙子任务则展开，只看没有子任务的子任务或孙子任务的状态。

不设置开始结束时间可以用来当分组功能用

### 2）重复、阶段、定期任务

次数未满有完成一次和取消完成一次，满了只有取消完成一次和删除

### 3）勾选

勾选则设置状态为完成，父任务勾选为已完成会使子任务的状态全部设置为完成。与上述完成一次导致的已完成不同，该状态会停止非一次性任务的自动更新，并且不能进行除了删除以外的操作，除非取消勾选。

子任务有完成状态（包括完成一次导致的已完成）会使父任务的勾选状态显示为部分完成

### 4）编辑任务

不能修改任务类型，将日期设为2000/1/1以取消开始和结束时间。

## 3.任务

### 1）一次性任务

开始和结束时间都能不设，完成了就是完成了。

### 2）重复任务

时间同上，可以设置需要完成的次数，右键完成一次就完成一次，完成次数达到需要完成的次数则完成。

### 3）定期任务

不设更新时间默认以当天零点或者第二天零点为起点计算下一次更新时间，设置更新时间则直接设置为下一次更新的时间。

到达开始时间自动更新时间并增加需要完成的次数。完成后不再更新

显示的开始时间为下一次更新的时间，即编辑和数据库里的开始时间

### 4）阶段任务

不设开始时间默认为当天所在阶段的首日，次数显示连续完成的阶段数，上个阶段未完成则归零。

### 注：更新只会在重新打开软件时发生
