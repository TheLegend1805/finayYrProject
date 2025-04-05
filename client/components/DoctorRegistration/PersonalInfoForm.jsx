import { useState } from "react";
import React from "react";

const PersonalInfoForm = ({ data, updateData }) => {
  const [form, setForm] = useState(data);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "image/jpeg") {
      setForm({ ...form, profilePhoto: file });
    } else {
      alert("Please upload a valid .jpg file.");
    }
  };

  const handleBlur = () => {
    updateData("personal_info", form);
  };

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Personal Information</h2>

      <div>
        <label className="block font-medium">Full Name</label>
        <input
          type="text"
          name="fullName"
          value={form.fullName}
          onChange={handleChange}
          onBlur={handleBlur}
          className="w-full p-2 border rounded"
          required
        />
      </div>

      <div>
        <label className="block font-medium">Email</label>
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          onBlur={handleBlur}
          className="w-full p-2 border rounded"
          required
        />
      </div>

      <div>
        <label className="block font-medium">Phone</label>
        <input
          type="tel"
          name="phone"
          value={form.phone}
          onChange={handleChange}
          onBlur={handleBlur}
          className="w-full p-2 border rounded"
          required
        />
      </div>

      <div>
        <label className="block font-medium">Gender</label>
        <select
          name="gender"
          value={form.gender}
          onChange={handleChange}
          onBlur={handleBlur}
          className="w-full p-2 border rounded"
          required
        >
          <option value="">Select</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>
      </div>

      <div>
        <label className="block font-medium">Date of Birth</label>
        <input
          type="date"
          name="dob"
          value={form.dob}
          onChange={handleChange}
          onBlur={handleBlur}
          className="w-full p-2 border rounded"
          required
        />
      </div>

      <div>
        <label className="block font-medium">Profile Photo (.jpg only)</label>
        <input
          type="file"
          accept=".jpg"
          onChange={handleFileChange}
          className="w-full p-2 border rounded"
        />
      </div>
    </div>
  );
};

export default PersonalInfoForm;
