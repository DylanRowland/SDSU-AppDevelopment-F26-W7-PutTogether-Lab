// FormEvent describes the browser form event; hooks store state and run startup work.
import { FormEvent, useEffect, useState } from "react";

// This type mirrors the safe UserResponse returned by FastAPI.
type User = { user_id: number; username: string; email: string };

// Vite replaces this value during the frontend image build.
// LAB BREAKPOINT: the fallback is intentionally the wrong port.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8001";

export default function App() {
  // Store rows returned by GET /api/users.
  const [users, setUsers] = useState<User[]>([]);

  // null means create mode; an ID means edit/update mode.
  const [selectedId, setSelectedId] = useState<number | null>(null);

  // These values are controlled by the three form inputs.
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Show connection and CRUD results to the student.
  const [message, setMessage] = useState("Frontend is running. Backend is not connected yet.");

  // One helper keeps all HTTP requests consistent.
  async function request(path: string, options?: RequestInit) {
    // fetch sends a request from the browser to FastAPI.
    const response = await fetch(`${API_BASE_URL}${path}`, {
      // Tell FastAPI that request bodies contain JSON.
      headers: { "Content-Type": "application/json" },
      // Spread in the method and body supplied by the CRUD function.
      ...options,
    });

    // Convert non-2xx responses into a message handled by the caller.
    if (!response.ok) throw new Error(`Request failed with status ${response.status}`);

    // DELETE returns 204 with no JSON body; other operations return JSON.
    return response.status === 204 ? null : response.json();
  }

  // READ: load all users from the backend.
  async function readUsers() {
    try {
      setUsers(await request("/api/users"));
      setMessage("Users loaded.");
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Read failed.");
    }
  }

  // CREATE or UPDATE: the selected ID determines which operation is sent.
  async function submitUser(event: FormEvent<HTMLFormElement>) {
    // Prevent the browser from reloading the page after form submission.
    event.preventDefault();

    // No selected ID means POST/create; an ID means PUT/update.
    const method = selectedId === null ? "POST" : "PUT";
    const path = selectedId === null ? "/api/users" : `/api/users/${selectedId}`;

    try {
      // Send the form values as JSON to FastAPI.
      await request(path, { method, body: JSON.stringify({ username, email, password }) });
      setMessage(selectedId === null ? "User created." : "User updated.");
      clearForm();
      // Read again so the table displays the database's current rows.
      await readUsers();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Save failed.");
    }
  }

  // DELETE: remove one user by ID and reload the table.
  async function deleteUser(userId: number) {
    try {
      await request(`/api/users/${userId}`, { method: "DELETE" });
      setMessage("User deleted.");
      await readUsers();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "Delete failed.");
    }
  }

  // Put the selected row into the form so the same form can update it.
  function editUser(user: User) {
    setSelectedId(user.user_id);
    setUsername(user.username);
    setEmail(user.email);
    setPassword("");
    setMessage(`Editing user ${user.user_id}. Enter a new password to update it.`);
  }

  // Return the form to create mode and clear all input values.
  function clearForm() {
    setSelectedId(null);
    setUsername("");
    setEmail("");
    setPassword("");
  }

  // Read the database once when the page first loads.
  useEffect(() => {
    void readUsers();
  }, []);

  return (
    <main className="container py-4">
      <h1>CampusCatalog Users</h1>
      <p className="text-secondary">React + FastAPI + PostgreSQL + Docker</p>
      <div className="alert alert-secondary">{message}</div>

      {/* The first card contains both the create and update form. */}
      <div className="card mb-4">
        <div className="card-body">
          <h2 className="h4">{selectedId === null ? "Create user" : "Update user"}</h2>
          <form className="row g-3" onSubmit={submitUser}>
            <div className="col-md-4">
              <label className="form-label">Username</label>
              <input className="form-control" value={username} onChange={(event) => setUsername(event.target.value)} required />
            </div>
            <div className="col-md-4">
              <label className="form-label">Email</label>
              <input className="form-control" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
            </div>
            <div className="col-md-4">
              <label className="form-label">Password</label>
              <input className="form-control" type="password" value={password} onChange={(event) => setPassword(event.target.value)} minLength={8} required />
            </div>
            <div className="col-12">
              <button className="btn btn-primary me-2" type="submit">
                {selectedId === null ? "Create" : "Update"}
              </button>
              {selectedId !== null && <button className="btn btn-secondary" type="button" onClick={clearForm}>Cancel</button>}
            </div>
          </form>
        </div>
      </div>

      {/* The second card displays READ results and provides UPDATE/DELETE actions. */}
      <div className="card">
        <div className="card-body">
          <div className="d-flex justify-content-between align-items-center">
            <h2 className="h4">Read users</h2>
            <button className="btn btn-outline-primary" onClick={() => void readUsers()}>Refresh</button>
          </div>
          <div className="table-responsive mt-3">
            <table className="table table-striped">
              <thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Actions</th></tr></thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.user_id}>
                    <td>{user.user_id}</td><td>{user.username}</td><td>{user.email}</td>
                    <td>
                      <button className="btn btn-sm btn-outline-secondary me-2" onClick={() => editUser(user)}>Edit</button>
                      <button className="btn btn-sm btn-outline-danger" onClick={() => void deleteUser(user.user_id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  );
}
