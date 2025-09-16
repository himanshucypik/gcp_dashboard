// Fetch button for Instances & Buckets
document.getElementById("btnFetch").addEventListener("click", async () => {
  const projectId = document.getElementById("projectId").value.trim();
  if (!projectId) {
    alert("⚠️ Please enter a Project ID first!");
    return;
  }

  try {
    // Fetch instances
    const instancesRes = await fetch(`/api/instances/${projectId}`);
    const instancesData = await instancesRes.json();

    // Fill instances table
    const instancesBody = document.getElementById("instances");
    instancesBody.innerHTML = "";
    if (instancesData.length === 0) {
      instancesBody.innerHTML = `<tr><td colspan="4" class="text-center">No instances found</td></tr>`;
    } else {
      instancesData.forEach(inst => {
        instancesBody.innerHTML += `
          <tr>
            <td>${inst.name}</td>
            <td>${inst.zone}</td>
            <td>${inst.status}</td>
            <td>${inst.machineType}</td>
          </tr>
        `;
      });
    }


    // Fetch buckets
    const bucketsRes = await fetch(`/api/buckets/${projectId}`);
    const bucketsData = await bucketsRes.json();

    // Fill buckets table
    const bucketsBody = document.getElementById("buckets");
    bucketsBody.innerHTML = "";
    if (bucketsData.length === 0) {
      bucketsBody.innerHTML = `<tr><td colspan="3" class="text-center">No buckets found</td></tr>`;
    } else {
      bucketsData.forEach(bucket => {
        bucketsBody.innerHTML += `
          <tr>
            <td>${bucket.name}</td>
            <td>${bucket.location}</td>
            <td>${bucket.created}</td>
          </tr>
        `;
      });
    }

  } catch (err) {
    console.error("Error fetching data:", err);
    alert("❌ Failed to fetch data. Check console.");
  }
});

// Fetch button for Projects
document.getElementById("btnListProjects").addEventListener("click", async () => {
  try {
    const res = await fetch(`/api/projects`);
    const projectsData = await res.json();

    // Fill projects table
    const projectsBody = document.getElementById("projects");
    projectsBody.innerHTML = "";
    if (projectsData.length === 0) {
      projectsBody.innerHTML = `<tr><td colspan="3" class="text-center">No projects found</td></tr>`;
    } else {
      projectsData.forEach(p => {
        projectsBody.innerHTML += `
          <tr>
            <td>${p.projectId}</td>
            <td>${p.name}</td>
            <td>${p.number}</td>
          </tr>
        `;
      });
    }
  } catch (err) {
    console.error("Error fetching projects:", err);
    alert("❌ Failed to fetch projects. Check console.");
  }
});
