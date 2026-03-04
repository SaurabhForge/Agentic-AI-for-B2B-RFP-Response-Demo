document.addEventListener("DOMContentLoaded", () => {
    const runBtn = document.getElementById("run-btn");
    const refreshBtn = document.getElementById("refresh-btn");
    const outputDisplay = document.getElementById("output-display");

    // Agent Cards
    const agents = [
        document.getElementById("agent-sales"),
        document.getElementById("agent-tech"),
        document.getElementById("agent-price"),
        document.getElementById("agent-orch")
    ];

    // Reset UI to default state
    const resetAgents = () => {
        agents.forEach(agent => {
            agent.classList.remove("active", "success");
            agent.querySelector(".status-indicator").textContent = "IDLE";
        });
    };

    // Simulate agent progressing (For UI Visuals during the backend call)
    // The backend is synchronous so we'll fake the UI steps for aesthetic feedback
    const simulateAgentActivity = async () => {
        for (let i = 0; i < agents.length; i++) {
            const agent = agents[i];

            // Set Active
            agent.classList.add("active");
            agent.querySelector(".status-indicator").textContent = "WORKING...";

            // Wait a bit (simulate time taken by agent)
            await new Promise(res => setTimeout(res, 1200 + Math.random() * 800));

            // Set Success
            agent.classList.remove("active");
            agent.classList.add("success");
            agent.querySelector(".status-indicator").textContent = "COMPLETE";
        }
    };

    // Trigger the actual Backend execution
    const runSystem = async () => {
        if (runBtn.disabled) return;

        // UI Preparation
        runBtn.disabled = true;
        runBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i><span>Orchestrating...</span>`;
        outputDisplay.innerHTML = `<div class="placeholder-text"><i class="fa-solid fa-circle-notch fa-spin"></i> System running... please wait.</div>`;
        resetAgents();

        try {
            // Start UI animation loop
            const animationPromise = simulateAgentActivity();

            // Start API Request
            const response = await fetch('/api/run', { method: 'POST' });
            const data = await response.json();

            // Wait for both frontend animations and backend logic to finish
            await animationPromise;

            if (data.status === "success" && data.content) {
                outputDisplay.textContent = data.content;
            } else if (data.status === "success") {
                await fetchResults();
            } else {
                outputDisplay.innerHTML = `<div style="color: #ef4444;">Error: ${data.message}</div>`;
            }
        } catch (error) {
            outputDisplay.innerHTML = `<div style="color: #ef4444;">Connection Error: Could not reach the orchestrator API.</div>`;
            console.error(error);
        } finally {
            // Reset Button
            runBtn.disabled = false;
            runBtn.innerHTML = `<i class="fa-solid fa-play"></i><span>Run Agentic System</span>`;
        }
    };

    // Fetch and display the results from output directory
    const fetchResults = async () => {
        refreshBtn.classList.add("rotating");
        try {
            const res = await fetch('/api/results');
            const data = await res.json();

            if (data.content) {
                // Escape HTML to display text safely, and preserve whitespace
                outputDisplay.textContent = data.content;
            } else {
                outputDisplay.innerHTML = `<div class="placeholder-text">No results found yet.</div>`;
            }
        } catch (error) {
            outputDisplay.innerHTML = `<div style="color: #ef4444;">Failed to load results.</div>`;
            console.error(error);
        } finally {
            setTimeout(() => refreshBtn.classList.remove("rotating"), 500);
        }
    };

    // Event Listeners
    runBtn.addEventListener("click", runSystem);
    refreshBtn.addEventListener("click", fetchResults);

    // Initial load
    fetchResults();
});
