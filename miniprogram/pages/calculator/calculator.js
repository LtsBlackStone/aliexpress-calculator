const app = getApp()

Page({
  data: {
    // 输入字段
    cost: '',
    shipping: '',
    commission: '10',
    marketing: '5',
    margin: '20',
    discount: '0',
    exchangeRate: '7.20',

    // 计算结果
    price: '0.00',
    profit: '0.00',
    backendPrice: '0.00',
    usdPrice: '0.00',

    // 结果颜色
    priceColor: 'color-default',
    profitColor: 'color-default',
    backendPriceColor: 'color-default',
    usdPriceColor: 'color-default',

    // 错误信息
    errorMsg: ''
  },

  onLoad: function () {
    const defaults = app.globalData.defaults
    this.setData({
      commission: defaults.commission,
      marketing: defaults.marketing,
      margin: defaults.margin,
      discount: defaults.discount,
      exchangeRate: defaults.exchangeRate
    })
  },

  onInputChange: function (e) {
    const field = e.currentTarget.dataset.field
    const value = e.detail.value
    this.setData({
      [field]: value
    })
  },

  calculate: function () {
    this.setData({ errorMsg: '' })

    const costStr = (this.data.cost || '').trim()
    const shippingStr = (this.data.shipping || '').trim()

    if (!costStr || !shippingStr) {
      this._displayError('请输入产品成本和国际运费')
      return
    }

    const cost = parseFloat(costStr)
    const shipping = parseFloat(shippingStr)

    if (isNaN(cost) || isNaN(shipping)) {
      this._displayError('请输入有效的数字')
      return
    }

    const commission = parseFloat(this.data.commission || '0') / 100
    const marketing = parseFloat(this.data.marketing || '0') / 100
    const margin = parseFloat(this.data.margin || '0') / 100

    if (isNaN(commission) || isNaN(marketing) || isNaN(margin)) {
      this._displayError('请输入有效的数字')
      return
    }

    // 检查分母
    const denominator = 1 - commission - marketing - margin
    if (denominator <= 0) {
      this._displayError('费率之和不能大于或等于100%，请调整参数')
      return
    }

    // 核心公式：售价 = (国际运费 + 产品成本) / (1 - 平台佣金率 - 营销费率 - 毛利率)
    const price = (shipping + cost) / denominator

    // 利润计算
    const profit = price - cost - shipping - (price * commission) - (price * marketing)

    // 后台定价
    const discount = parseFloat(this.data.discount || '0') / 100
    if (isNaN(discount)) {
      this._displayError('请输入有效的折扣率')
      return
    }
    if (discount >= 1) {
      this._displayError('单品折扣率不能大于或等于100%')
      return
    }
    const backendPrice = discount > 0 ? price / (1 - discount) : price

    // 美元定价
    const exchangeRate = parseFloat(this.data.exchangeRate || '0')
    if (isNaN(exchangeRate) || exchangeRate <= 0) {
      this._displayError('请输入有效的美元汇率（大于0）')
      return
    }
    const usdPrice = backendPrice / exchangeRate

    this._displayResult(price, profit, backendPrice, usdPrice)
  },

  _displayResult: function (price, profit, backendPrice, usdPrice) {
    const profitColor = profit >= 0 ? 'color-green' : 'color-red'

    this.setData({
      price: price.toFixed(2),
      profit: profit.toFixed(2),
      backendPrice: backendPrice.toFixed(2),
      usdPrice: usdPrice.toFixed(2),
      priceColor: 'color-blue',
      profitColor: profitColor,
      backendPriceColor: 'color-blue',
      usdPriceColor: 'color-blue',
      errorMsg: ''
    })
  },

  _displayError: function (message) {
    this.setData({
      price: '0.00',
      profit: '0.00',
      backendPrice: '0.00',
      usdPrice: '0.00',
      priceColor: 'color-default',
      profitColor: 'color-default',
      backendPriceColor: 'color-default',
      usdPriceColor: 'color-default',
      errorMsg: message
    })
  },

  reset: function () {
    const defaults = app.globalData.defaults
    this.setData({
      cost: '',
      shipping: '',
      commission: defaults.commission,
      marketing: defaults.marketing,
      margin: defaults.margin,
      discount: defaults.discount,
      exchangeRate: defaults.exchangeRate,
      price: '0.00',
      profit: '0.00',
      backendPrice: '0.00',
      usdPrice: '0.00',
      priceColor: 'color-default',
      profitColor: 'color-default',
      backendPriceColor: 'color-default',
      usdPriceColor: 'color-default',
      errorMsg: ''
    })
  }
})
