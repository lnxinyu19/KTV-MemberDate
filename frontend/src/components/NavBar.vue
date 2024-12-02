<script setup>
const menuItems = [
    {
        path: '/PartyWorldMember',
        name: '錢櫃',
    },
    {
        path: '/HolidayMember',
        name: '好樂迪'
    },
]
</script>
<template>
    <nav class="bg-base-100 flex justify-center sticky top-0 z-10">
        <ul class="menu menu-horizontal ">
            <li v-for="(menuItem, index) in menuItems" :key="`menuItem__${index}`" class="text-center">
                <RouterLink :to="menuItem.path">{{ menuItem.name }}</RouterLink>
            </li>
        </ul>
    </nav>
</template>