document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('travelForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsContainer = document.getElementById('resultsContainer');
    const itineraryContainer = document.getElementById('itineraryContainer');
    const tipsContent = document.getElementById('tipsContent');
    const essentialContent = document.getElementById('essentialContent');
    const errorMessage = document.getElementById('errorMessage');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading indicator and hide results
        loadingIndicator.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        errorMessage.classList.add('hidden');

        // Gather form data
        const formData = {
            answers: {
                Experiences: form.querySelector('#experiences').value.split(',').map(item => item.trim()),
                totalDays: form.querySelector('#totalDays').value,
                'Places U want': form.querySelector('#places').value.split(',').map(item => item.trim()),
                activities: form.querySelector('#activities').value.split(',').map(item => item.trim()),
                season: form.querySelector('#season').value,
                budget: form.querySelector('#budget').value + ' EGP'
            }
        };

        try {
            // Make API call
            const response = await fetch('http://localhost:5000/api/generate-travel-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate travel plan');
            }

            // Display results
            displayResults(data);
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        } finally {
            loadingIndicator.classList.add('hidden');
        }
    });

    function displayResults(data) {
        resultsContainer.classList.remove('hidden');

        // Display Itinerary
        if (data.travel_plan && data.travel_plan.itinerary) {
            const itinerary = data.travel_plan.itinerary;
            let itineraryHTML = '';

            // Display days
            itinerary.days.forEach((day, index) => {
                const dayData = day[`day${index + 1}`];
                itineraryHTML += `
                    <div class="border-l-4 border-blue-500 pl-4 mb-6">
                        <h3 class="text-xl font-semibold mb-2">Day ${index + 1}</h3>
                        <div class="space-y-3">
                            <div>
                                <h4 class="font-medium text-blue-600">${dayData.location.name}</h4>
                                <p class="text-gray-600">${dayData.location.description}</p>
                            </div>
                            <div class="grid grid-cols-2 gap-4 text-sm">
                                <div>
                                    <span class="font-medium">Entry Fee:</span> ${dayData.location.entry_fee}
                                </div>
                                <div>
                                    <span class="font-medium">Duration:</span> ${dayData.location.duration}
                                </div>
                                <div>
                                    <span class="font-medium">Open:</span> ${dayData.location.open_time}
                                </div>
                                <div>
                                    <span class="font-medium">Close:</span> ${dayData.location.close_time}
                                </div>
                            </div>
                            <div class="bg-blue-50 p-3 rounded-md">
                                <p class="text-sm text-blue-800"><span class="font-medium">Cultural Tip:</span> ${dayData.cultural_tip}</p>
                            </div>
                        </div>
                    </div>
                `;
            });

            // Display budget breakdown
            if (itinerary.budget_breakdown) {
                itineraryHTML += `
                    <div class="mt-6 p-4 bg-gray-50 rounded-lg">
                        <h3 class="text-lg font-semibold mb-3">Budget Breakdown</h3>
                        <div class="grid grid-cols-2 gap-4 text-sm">
                            <div><span class="font-medium">Attractions:</span> ${itinerary.budget_breakdown.attractions}</div>
                            <div><span class="font-medium">Transport:</span> ${itinerary.budget_breakdown.estimated_transport}</div>
                            <div><span class="font-medium">Meals:</span> ${itinerary.budget_breakdown.estimated_meals}</div>
                            <div><span class="font-medium">Contingency:</span> ${itinerary.budget_breakdown.contingency}</div>
                        </div>
                    </div>
                `;
            }

            itineraryContainer.innerHTML = itineraryHTML;
        }

        // Display Travel Tips
        if (data.travel_plan && data.travel_plan.additional_info) {
            const info = data.travel_plan.additional_info;
            let tipsHTML = '';

            // Weather recommendations
            if (info.weather_recommendations) {
                tipsHTML += `
                    <div class="mb-6">
                        <h4 class="font-semibold text-lg mb-2">Weather Tips</h4>
                        <div class="space-y-2">
                            <p><span class="font-medium">Best Times:</span> ${info.weather_recommendations.best_times}</p>
                            <div>
                                <p class="font-medium mb-1">What to Wear:</p>
                                <ul class="list-disc list-inside text-sm">
                                    ${info.weather_recommendations.what_to_wear.map(item => `<li>${item}</li>`).join('')}
                                </ul>
                            </div>
                            <div>
                                <p class="font-medium mb-1">What to Bring:</p>
                                <ul class="list-disc list-inside text-sm">
                                    ${info.weather_recommendations.what_to_bring.map(item => `<li>${item}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                `;
            }

            // Cultural etiquette
            if (info.cultural_etiquette) {
                tipsHTML += `
                    <div>
                        <h4 class="font-semibold text-lg mb-2">Cultural Etiquette</h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <p class="font-medium mb-1">Dress Code:</p>
                                <ul class="list-disc list-inside text-sm">
                                    ${info.cultural_etiquette.dress_code.map(item => `<li>${item}</li>`).join('')}
                                </ul>
                            </div>
                            <div>
                                <p class="font-medium mb-1">Social Customs:</p>
                                <ul class="list-disc list-inside text-sm">
                                    ${info.cultural_etiquette.social_customs.map(item => `<li>${item}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                `;
            }

            // Transportation tips
            if (info.transportation) {
                tipsHTML += `
                    <div class="mt-6">
                        <h4 class="font-semibold text-lg mb-2">Transportation Tips</h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <p class="font-medium mb-1">Getting Around:</p>
                                <ul class="list-disc list-inside text-sm">
                                    ${info.transportation.getting_around.map(item => `<li>${item}</li>`).join('')}
                                </ul>
                            </div>
                            <div>
                                <p class="font-medium mb-1">Travel Tips:</p>
                                <ul class="list-disc list-inside text-sm">
                                    ${info.transportation.tips.map(item => `<li>${item}</li>`).join('')}
                                </ul>
                            </div>
                            <div>
                                <p class="font-medium mb-1">Safety While Traveling:</p>
                                <ul class="list-disc list-inside text-sm">
                                    ${info.transportation.safety.map(item => `<li>${item}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                `;
            }

            tipsContent.innerHTML = tipsHTML;

            // Display Essential Information
            let essentialHTML = '';

            // Emergency contacts
            if (info.emergency_contacts) {
                essentialHTML += `
                    <div class="mb-6">
                        <h4 class="font-semibold text-lg mb-2">Emergency Contacts</h4>
                        <div class="grid grid-cols-2 gap-2 text-sm">
                            ${Object.entries(info.emergency_contacts).map(([key, value]) => `
                                <div>
                                    <span class="font-medium">${key.replace('_', ' ').toUpperCase()}:</span> ${value}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            // Useful phrases
            if (info.useful_phrases) {
                essentialHTML += `
                    <div>
                        <h4 class="font-semibold text-lg mb-2">Useful Arabic Phrases</h4>
                        <div class="grid grid-cols-2 gap-2 text-sm">
                            ${Object.entries(info.useful_phrases).map(([key, value]) => `
                                <div>
                                    <span class="font-medium">${key.replace('_', ' ')}:</span> ${value}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                `;
            }

            essentialContent.innerHTML = essentialHTML;
        }

        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
}); 