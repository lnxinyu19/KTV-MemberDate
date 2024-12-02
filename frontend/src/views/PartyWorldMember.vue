<script setup lang="ts">
import { onMounted, ref, computed } from 'vue';
import { months, isCurrentMonth, currentYear, currentMonth } from '@/utils/months';

interface IGetPartyWorldData {
    [key: string]: IPartyWorldTableData[],

}
interface IPartyWorldTableData {
    store: string,
    member_date: string[]
}

const tableData = ref<IGetPartyWorldData>({})

const yearOptions = ref<string[]>([])
const selectedYear = ref<string>(currentYear.toString())
const selectedStore = ref("")
const markList = ref<Set<number>>(new Set());
const filterTableData = computed(() => {
    if (selectedYear.value) {
        return tableData.value[selectedYear.value]
    }
})

const toggleMark = (month: number) => {
    markList.value.has(month)
        ? markList.value.delete(month)
        : markList.value.add(month);
}
const toggleSelectStore = (store: string) => {
    if (selectedStore.value === store) {
        selectedStore.value = ""
    } else {
        selectedStore.value = store
    }
}

const clearMark = () => {
    markList.value.clear()
    selectedStore.value = ""
}

const getMemberDateTable = async () => {
    try {
        const response = await fetch('/api/party_world_data')
        const data = await response.json()

        yearOptions.value = Object.keys(data)
        tableData.value = data

    } catch (error) {
        console.error(error)
    }
}

onMounted(async () => {
    await getMemberDateTable()
})
</script>
<template>
    <div class="flex-col md:flex items-center justify-center w-screen max-w-screen-xl">
        <div class="flex flex-col md:flex-row items-center justify-around w-72 gap-y-4">
            <div class="flex items-center justify-center w-full">
                <label for="select_area">年份：</label>
                <select id="select_area" class="select select-bordered w-3/4" v-model="selectedYear">
                    <option v-for="(year, index) in yearOptions" :key="`year__${index}`" :value="year">{{ year }}
                    </option>
                </select>
            </div>
        </div>

        <div class="space-y-4 mt-10 px-4 w-full">
            <div class="flex justify-between items-center mb-2">
                <h2 class="text-xl font-bold">{{ selectedYear }}</h2>
                <button class="btn btn-secondary text-white" @click="clearMark">清除已選取</button>
            </div>
            <div class="rounded-xl overflow-x-auto">
                <table class="table">
                    <thead>
                        <tr class="bg-base-200">
                            <th class="border border-gray-300 px-4 py-2 sticky left-0 z-10 bg-base-200" align="center">
                                門市</th>
                            <th class="border border-gray-300 px-4 py-2 cursor-pointer" align="center"
                                v-for="(month, index) in months" :key="index" @click="toggleMark(month.value)"
                                :class="{ 'bg-accent text-white font-bold text-lg': isCurrentMonth(month.value) || markList.has(month.value) }">
                                {{ month.label }}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(detail, index) in filterTableData" :key="index">
                            <td class="border border-gray-300 px-4 py-2 text-base transition-all duration-500 sticky left-0 z-10 cursor-pointer"
                                align="center" width="150" :class="{
                                    'text-xl bg-accent text-white font-bold': selectedStore === detail.store,
                                    'bg-base-200': selectedStore !== detail.store
                                }" @click="toggleSelectStore(detail.store)">
                                {{ detail.store }}</td>
                            <td class="border border-gray-300 px-4 py-2 text-center overflow-hidden transition-all duration-500"
                                :class="{ 'bg-accent text-white font-bold text-lg': isCurrentMonth(monthIndex + 1) || markList.has(monthIndex + 1) || selectedStore === detail.store }"
                                v-for="(value, monthIndex) in detail.member_date" :key="monthIndex">
                                {{ value }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>