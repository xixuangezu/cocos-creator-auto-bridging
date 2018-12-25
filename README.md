# cocos creator auto bridging for lua
cocos2dx-lua 调用creator代码 自动生成工具
### 依赖
Cheetah模块
```
pip install Cheetah==2.4.4
```
### 用法
1. 在csv/UiConfig.csv配置页面名称/类型,类型分类见doc.txt
2. 运行index.py
3. 在out目录会生成对应lua文件
### 特化
本工具现根据个人工程进行特化, 使用者需根据自己工程自行调整
1. 源码见 src 目录
2. src/generator.py -> <Generator::generate_code> 是解析逻辑
3. 模板见 model 目录