"""
速卖通（AliExpress）跨境电商定价计算器
核心公式：售价 = (国际运费 + 产品成本) / (1 - 平台佣金率 - 营销费率 - 毛利率)
"""

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont


# 默认值
DEFAULTS = {
    "commission": "10",
    "marketing": "5",
    "margin": "20",
    "discount": "0",
}

WINDOW_TITLE = "速卖通定价计算器"
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 620


class AliExpressCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)

        # 设置主题
        self.style = ttk.Style()
        try:
            self.style.theme_use("vista")
        except tk.TclError:
            pass

        # 设置字体
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(size=10, family="Microsoft YaHei UI")
        self.root.option_add("*Font", self.default_font)

        # 输入变量
        self.cost_var = tk.StringVar()
        self.shipping_var = tk.StringVar()
        self.commission_var = tk.StringVar(value=DEFAULTS["commission"])
        self.marketing_var = tk.StringVar(value=DEFAULTS["marketing"])
        self.margin_var = tk.StringVar(value=DEFAULTS["margin"])
        self.discount_var = tk.StringVar(value=DEFAULTS["discount"])

        # 构建界面
        self._create_widgets()
        self._center_window()

    def _center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - WINDOW_WIDTH) // 2
        y = (self.root.winfo_screenheight() - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

    def _validate_numeric(self, value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False

    def _create_widgets(self):
        vcmd = (self.root.register(self._validate_numeric), "%P")

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ========== 顶部品牌标识 ==========
        tk.Label(
            main_frame,
            text="天民电商出品",
            font=("Microsoft YaHei UI", 12, "bold"),
            fg="#c0392b",
        ).pack(fill=tk.X, pady=(0, 2))

        tk.Label(
            main_frame,
            text="速卖通星球号：97679310",
            font=("Microsoft YaHei UI", 10, "bold"),
            fg="#c0392b",
        ).pack(fill=tk.X, pady=(0, 10))

        # ========== 输入参数区域 ==========
        input_frame = ttk.LabelFrame(main_frame, text=" 输入参数 ", padding=(20, 15))
        input_frame.pack(fill=tk.X, pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)

        fields = [
            ("产品成本 (元):", self.cost_var),
            ("国际运费 (元):", self.shipping_var),
            ("平台佣金率 (%):", self.commission_var),
            ("营销费率 (%):", self.marketing_var),
            ("目标毛利率 (%):", self.margin_var),
            ("单品折扣率 (%):", self.discount_var),
        ]

        for i, (label_text, var) in enumerate(fields):
            label = ttk.Label(input_frame, text=label_text, width=16, anchor="e")
            label.grid(row=i, column=0, padx=(0, 10), pady=6, sticky="e")

            entry = ttk.Entry(
                input_frame,
                textvariable=var,
                validate="key",
                validatecommand=vcmd,
                width=25,
            )
            entry.grid(row=i, column=1, pady=6, sticky="ew")

        # ========== 按钮区域 ==========
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 15))

        self.style.configure(
            "Calc.TButton", font=("Microsoft YaHei UI", 11, "bold")
        )

        calc_btn = ttk.Button(
            btn_frame,
            text="开始计算",
            style="Calc.TButton",
            command=self.calculate,
            width=15,
        )
        calc_btn.pack(side=tk.LEFT, expand=True, padx=5)

        reset_btn = ttk.Button(
            btn_frame,
            text="重置",
            command=self.reset,
            width=15,
        )
        reset_btn.pack(side=tk.LEFT, expand=True, padx=5)

        # ========== 计算结果区域 ==========
        result_frame = ttk.LabelFrame(main_frame, text=" 计算结果 ", padding=(20, 20))
        result_frame.pack(fill=tk.X)
        result_frame.columnconfigure(1, weight=1)

        result_font = tkfont.Font(family="Microsoft YaHei UI", size=16, weight="bold")

        ttk.Label(result_frame, text="建议零售价:", font=("Microsoft YaHei UI", 11)).grid(
            row=0, column=0, padx=(0, 10), pady=10, sticky="e"
        )
        self.price_label = ttk.Label(
            result_frame, text="¥ 0.00", font=result_font, foreground="#333333"
        )
        self.price_label.grid(row=0, column=1, pady=10, sticky="w")

        ttk.Label(result_frame, text="预估利润:", font=("Microsoft YaHei UI", 11)).grid(
            row=1, column=0, padx=(0, 10), pady=10, sticky="e"
        )
        self.profit_label = ttk.Label(
            result_frame, text="¥ 0.00", font=result_font, foreground="#333333"
        )
        self.profit_label.grid(row=1, column=1, pady=10, sticky="w")

        ttk.Label(result_frame, text="后台定价:", font=("Microsoft YaHei UI", 11)).grid(
            row=2, column=0, padx=(0, 10), pady=10, sticky="e"
        )
        self.backend_price_label = ttk.Label(
            result_frame, text="¥ 0.00", font=result_font, foreground="#333333"
        )
        self.backend_price_label.grid(row=2, column=1, pady=10, sticky="w")

        # 错误/提示信息
        self.message_label = ttk.Label(
            main_frame, text="", foreground="#c0392b", font=("Microsoft YaHei UI", 9)
        )
        self.message_label.pack(pady=(10, 0))


    def calculate(self):
        self.message_label.config(text="")

        try:
            # 检查必填字段
            cost_str = self.cost_var.get().strip()
            shipping_str = self.shipping_var.get().strip()

            if not cost_str or not shipping_str:
                self._display_error("请输入产品成本和国际运费")
                return

            cost = float(cost_str)
            shipping = float(shipping_str)
            commission = float(self.commission_var.get() or "0") / 100
            marketing = float(self.marketing_var.get() or "0") / 100
            margin = float(self.margin_var.get() or "0") / 100

            # 检查分母
            denominator = 1 - commission - marketing - margin
            if denominator <= 0:
                self._display_error("费率之和不能大于或等于100%，请调整参数")
                return

            # 核心公式
            price = (shipping + cost) / denominator

            # 利润计算
            profit = price - cost - shipping - (price * commission) - (price * marketing)

            # 后台定价
            discount = float(self.discount_var.get() or "0") / 100
            if discount >= 1:
                self._display_error("单品折扣率不能大于或等于100%")
                return
            backend_price = price / (1 - discount) if discount > 0 else price

            self._display_result(price, profit, backend_price)

        except ValueError:
            self._display_error("请输入有效的数字")
        except Exception:
            self._display_error("计算出错，请检查输入")

    def _display_result(self, price, profit, backend_price):
        self.price_label.config(
            text=f"¥ {price:.2f}", foreground="#1a5276"
        )

        color = "#27ae60" if profit >= 0 else "#c0392b"
        self.profit_label.config(
            text=f"¥ {profit:.2f}", foreground=color
        )

        self.backend_price_label.config(
            text=f"¥ {backend_price:.2f}", foreground="#1a5276"
        )
        self.message_label.config(text="")

    def _display_error(self, message):
        self.price_label.config(text="¥ 0.00", foreground="#333333")
        self.profit_label.config(text="¥ 0.00", foreground="#333333")
        self.backend_price_label.config(text="¥ 0.00", foreground="#333333")
        self.message_label.config(text=message, foreground="#c0392b")

    def reset(self):
        self.cost_var.set("")
        self.shipping_var.set("")
        self.commission_var.set(DEFAULTS["commission"])
        self.marketing_var.set(DEFAULTS["marketing"])
        self.margin_var.set(DEFAULTS["margin"])
        self.discount_var.set(DEFAULTS["discount"])
        self.price_label.config(text="¥ 0.00", foreground="#333333")
        self.profit_label.config(text="¥ 0.00", foreground="#333333")
        self.backend_price_label.config(text="¥ 0.00", foreground="#333333")
        self.message_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = AliExpressCalculator(root)
    root.mainloop()
