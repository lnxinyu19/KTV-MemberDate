import { defineConfig, loadEnv } from 'vite';
import path from "path";
import vue from '@vitejs/plugin-vue';
// https://vite.dev/config/
export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, process.cwd(), 'VITE_');
    return {
        plugins: [vue()],
        resolve: {
            alias: {
                '@': path.resolve(__dirname, './src'), // 別名指向 src 資料夾
            },
        },
        server: {
            proxy: {
                '/api': {
                    target: `${env.VITE_API_URL}:${env.VITE_API_PORT}`,
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/api/, ''),
                },
            },
        },
    };
});
