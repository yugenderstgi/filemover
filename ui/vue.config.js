const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],devServer: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Replace with the actual backend API URL
        changeOrigin: true,
        pathRewrite: { '^/api': '' },
      },
    },
  },

})
