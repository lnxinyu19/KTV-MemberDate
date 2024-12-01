<script setup>
const menuItems = [
    {
        path: '/PartyWorldMember',
        name: 'Nav1',
    },
    {
        path: '/HolidayMember',
        name: 'Nav2'
    },
    {
        path: '/',
        name: '123'
    }
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