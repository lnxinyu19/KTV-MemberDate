<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { months, isCurrentMonth, currentMonth } from "@/utils/months";

interface IStoreMemberDate {
    store: string,
    member_date: string[]
}

interface IGetHolidayData {
    area: string,
    details: IStoreMemberDate[]
}

const areaOptions = ref<string[]>(['請選擇區域'])
const tableData = ref<IGetHolidayData[]>()
const markList = ref<Set<number>>(new Set());

const storeOptions = computed(() =>
    tableData.value?.find((item) => item.area === selectedArea.value)?.details.map((detail) => detail.store) || ['請先選擇區域']
);

const selectedArea = ref<string>(areaOptions.value[0])
const selectedStore = ref<string>(storeOptions.value[0])
const selectedMonth = ref<number>(months[currentMonth - 1].value)

const filterTableData = computed(() => {
    if (!selectedArea.value) {
        return tableData.value
    }
    if (selectedStore.value) {
        return tableData.value?.filter((item) => item.details.find((detail) => detail.store === selectedStore.value))
    }
})

const toggleMark = (month: number) => {
    markList.value.has(month)
        ? markList.value.delete(month)
        : markList.value.add(month);
}

const getMemberDateTable = async () => {
    try {
        const response = await fetch('/holiday_data')
        const data: IGetHolidayData[] = await response.json()
        const options = data.map((item) => item.area)
        areaOptions.value = areaOptions.value.concat(options);

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
        <div class="flex flex-col md:flex-row items-center justify-around w-full gap-y-4">
            <div class="flex items-center justify-center w-full">
                <label for="select_area">區域：</label>
                <select id="select_area" class="select select-bordered w-3/4" v-model="selectedArea"
                    @change="selectedStore = storeOptions[0]">
                    <option v-for="(area, index) in areaOptions" :key="`area__${index}`" :value="area">{{ area }}
                    </option>
                </select>
            </div>
            <div class="flex items-center justify-center w-full">
                <label for="select_store">門市：</label>
                <select id="select_store" class="select select-bordered w-3/4" v-model="selectedStore"
                    :disabled="storeOptions.length === 1">
                    <option v-for="(store, index) in storeOptions" :key="`store__${index}`" :value="store">{{ store }}
                    </option>
                </select>
            </div>
            <div class="flex items-center justify-center w-full">
                <label for="select_month">月份：</label>
                <select id="select_month" class="select select-bordered w-3/4" v-model="selectedMonth">
                    <option v-for="(month, index) in months" :key="`month__${index}`" :value="month.value">{{
                        month.label }}
                    </option>
                </select>
            </div>
        </div>

        <div class="space-y-4 mt-10 px-4 w-full">
            <div v-for="(region, regionIndex) in filterTableData" :key="regionIndex">
                <div class="flex justify-between items-center mb-2">
                    <h2 class="text-xl font-bold">{{ region.area }}</h2>
                    <!-- TODO 根據checkbox過濾掉一些表格資料? -->
                    <!-- <input type="checkbox" checked="checked" class="checkbox checkbox-sm" /> -->
                    <button class="btn btn-secondary text-white" @click="markList.clear()">清除已選取</button>
                </div>
                <div class="rounded-xl overflow-x-auto">
                    <table class="table">
                        <thead>
                            <tr class="bg-base-200">
                                <th class="border border-gray-300 px-4 py-2 sticky left-0 z-10 bg-base-200"
                                    align="center">
                                    門市</th>
                                <th class="border border-gray-300 px-4 py-2 cursor-pointer" align="center"
                                    v-for="(month, index) in months" :key="index" @click="toggleMark(month.value)"
                                    :class="{ 'bg-accent text-white font-bold text-lg': isCurrentMonth(month.value) || markList.has(month.value) }">
                                    {{ month.label }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(detail, index) in region.details" :key="index">
                                <td class="border border-gray-300 px-4 py-2 text-base transition-all duration-500 sticky left-0 z-10"
                                    align="center" width="150" :class="{
                                        'text-xl bg-accent text-white font-bold': selectedStore === detail.store,
                                        'bg-base-200': selectedStore !== detail.store
                                    }">
                                    {{ detail.store }}</td>
                                <td class="border border-gray-300 px-4 py-2 text-center overflow-hidden transition-all duration-500"
                                    :class="{ 'bg-accent text-white font-bold text-lg': isCurrentMonth(monthIndex + 1) || markList.has(monthIndex + 1) }"
                                    v-for="(value, monthIndex) in detail.member_date" :key="monthIndex">
                                    {{ value }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>