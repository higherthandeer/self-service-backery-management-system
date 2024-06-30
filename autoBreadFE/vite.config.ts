import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// svg用到的插件
import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import path from 'path'
// 引入mock
import { viteMockServe } from 'vite-plugin-mock'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
  return {
    plugins: [
      vue(),
      createSvgIconsPlugin({
        iconDirs: [path.resolve(process.cwd(), 'src/assets/icons')],
        symbolId: 'icon-[dir]-[name]',
      }),

      VueSetupExtend(),
    ],
    resolve: {
      alias: {
        '@': path.resolve('./src'), // 相对路径别名配置，使用 @ 代替 src
      },
    },
  }
})
