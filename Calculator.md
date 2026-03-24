**Subject:** 开发一个速卖通（AliExpress）跨境电商定价器桌面应用程序 & 微信小程序

**Context:**
我需要开发一个专门为速卖通卖家设计的定价计算器。该程序同时支持 Windows 桌面版（Python/Tkinter）和微信小程序版本，界面要求简洁直观。

**Core Formula (核心逻辑):**
售价 = (国际运费 + 产品成本) / (1 - 平台佣金率 - 营销费率 - 毛利率)

**Functional Requirements:**

1. **输入参数 (Input Fields):**
* **产品成本 (Product Cost):** 必填，用户输入。
* **国际运费 (International Shipping):** 必填，用户输入。
* **平台佣金率 (Commission %):** 默认值 10%，允许用户修改。
* **营销费率 (Marketing %):** 默认值 5%（包含联盟、金币、活动让利等），允许用户修改。
* **目标毛利率 (Profit Margin %):** 默认值 20%，允许用户修改。
* **单品折扣率 (Discount %):** 默认值 0%，允许用户修改。用于计算后台定价。
* **美元汇率 (1 USD = ? CNY):** 默认值 7.20，允许用户修改。用于将人民币定价转换为美元定价。


2. **计算功能:**
* 点击“开始计算”按钮后，根据公式自动得出“最终建议零售价”。
* 自动计算并显示“利润金额” = 售价 - 成本 - 运费 - (售价 * 佣金率) - (售价 * 营销费率)。
* 自动计算并显示“后台定价” = 售价 / (1 - 折扣率)。
* 自动计算并显示“美元定价” = 后台定价 / 美元汇率。


3. **交互优化:**
* 输入框应仅允许数字和小数点。
* 包含一个“重置”按钮，一键恢复默认值。
* 界面语言使用**中文**。



**Technical Stack:**

### 桌面版 (Desktop)
* 使用 **Python** 语言。
* GUI 库使用 **Tkinter**。
* 代码结构要清晰，包含错误处理（如分母不能为零或结果为负数的情况）。

### 微信小程序版 (WeChat Mini Program)
* 使用微信小程序原生框架开发。
* 项目文件位于 `miniprogram/` 目录。
* 在微信开发者工具中导入 `miniprogram/` 目录即可运行。

**项目结构 (Project Structure):**

```
aliexpress-calculator/
├── aliexpress_calculator.py          # 桌面版 Python 源代码
├── Calculator.md                      # 需求文档
├── .gitignore
└── miniprogram/                       # 微信小程序
    ├── app.js                         # 小程序入口
    ├── app.json                       # 小程序配置
    ├── app.wxss                       # 全局样式
    ├── project.config.json            # 项目配置
    ├── sitemap.json                   # 站点地图
    └── pages/
        └── calculator/
            ├── calculator.js          # 计算器页面逻辑
            ├── calculator.json        # 页面配置
            ├── calculator.wxml        # 页面模板
            └── calculator.wxss        # 页面样式
```

**Output Deliverables:**

1. 完整的 Python 源代码。
2. 完整的微信小程序源代码。
3. 详细的说明：告诉如何安装必要的依赖，以及使用什么命令将该 `.py` 文件打包成一个独立的 `.exe` 可执行文件（例如使用 PyInstaller）。
4. 微信小程序使用说明：在微信开发者工具中导入 `miniprogram/` 目录即可预览和调试。