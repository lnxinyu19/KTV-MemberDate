<script setup lang="ts">
import { onMounted } from 'vue';
import NavBar from '@/components/NavBar.vue';


onMounted(() => {
    // const result = await fetch('/api/holiday_data').then((res) => res.json())
    // console.log(result)
})
</script>

<template>
    <div data-theme="cupcake" class="w-screen h-screen overflow-scroll mx-auto bg-white">
        <NavBar></NavBar>
        <div class="mt-10">
            <router-view />
        </div>
    </div>
</template>
