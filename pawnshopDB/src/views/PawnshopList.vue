<template>
    <div
        class="fixed top-16 left-0 right-0 flex justify-center z-10"
        style="padding: 1%"
    >
        <div
            id="reload"
            class="transform translate-y-0 transition-transform duration-300 ease-in-out"
            hidden
        >
            <button
                class="btn btn-accent size-fit text-xl"
                @click="fetchPawnshops"
            >
                ↻ Refresh
            </button>
        </div>
    </div>
    <h1 class="text-4xl font-bold mb-4 flex justify-center my-6">
        Pawnshops List
    </h1>

    <div class="container mx-auto p-4">
        <div class="grid grid-flow-col justify-end pr-5 items-center">
            <div class="flex my-5">
                <input
                    v-model="searchKeyword"
                    @keydown.enter="fetchPawnshops"
                    class="input input-bordered gap-2 rounded-r-none"
                    placeholder="Search"
                />
                <button
                    @click="fetchPawnshops"
                    class="btn btn-secondary rounded-l-none"
                >
                    Search
                </button>
            </div>
        </div>
        <div v-if="pawnshops.length">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                    v-for="pawnshop in pawnshops"
                    :key="pawnshop.id"
                    class="card bg-base-300 hover:border-primary border-2 border-base-300 shadow-lg transition-all duration-150"
                >
                    <div class="card-body p-4" style="border-radius: 8px">
                        <h2
                            class="card-title text-2xl font-semibold line-clamp-1"
                        >
                            {{ pawnshop.name }}
                        </h2>
                        <p class="line-clamp-2">{{ pawnshop.description }}</p>
                        <!-- <p>
                            <strong>Address: </strong>
                            {{ pawnshop.address }}
                        </p> -->
                        <div class="card-actions justify-end">
                            <!-- <router-link
                                :to="{ path: `/pawnshops/${pawnshop.id}` }"
                            >
                                <button
                                    class="btn btn-secondary"
                                    @click="viewPawnshop(pawnshop.id)"
                                >
                                    View Details
                                </button>
                            </router-link> -->
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="mt-4">
            <div class="card bg-base-300 border-2 border-accent p-5">
                <div class="card-title text-2xl font-semibold">
                    No pawnshops found.
                </div>
                <div class="card-actions justify-end">
                    <!-- <router-link to="/create">
                        <button class="btn btn-accent">Add New Pawnshop</button>
                    </router-link> -->
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '@/api';

// Variable
const pawnshops = ref([]);
const isDarkTheme = ref(false);
const searchKeyword = ref('');

/**
 * Fetch Data
 */
const fetchPawnshops = async () => {
    try {
        const params = {};
        if (searchKeyword.value) {
            params.keyword = searchKeyword.value;
        }
        const response = await apiClient.get('/records/', { params });
        pawnshops.value = response.data;
        window.scrollTo(0, 0);

        const reloadButton = document.getElementById('reload');
        reloadButton.classList.remove('translate-y-0');
        reloadButton.classList.remove('translate-y-[100%]');
        setTimeout(reloadButton.setAttribute('hidden', 'true'));
    } catch (error) {
        console.error('Error fetching pawnshops:', error);
        if (error.response) {
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
        }
    }
};

onMounted(() => {
    fetchPawnshops();
    isDarkTheme.value = window.matchMedia(
        '(prefers-color-scheme: dark)'
    ).matches;
    window
        .matchMedia('(prefers-color-scheme: dark)')
        .addEventListener('change', (e) => {
            isDarkTheme.value = e.matches;
        });
});
</script>

<style scoped>
.line-clamp-2 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
}

.line-clamp-1 {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
