import { useState } from "react";
import PersonalInfoForm from "./PersonalInfoForm.jsx";
import ProfessionalInfoForm from "./ProfessionalInfoForm.jsx";
import VerificationInfoForm from "./VerificationInfoForm.jsx";
import { toast } from "react-toastify";
import React from "react";

const DoctorRegistration = () => {
  const [step, setStep] = useState(1);

  const [formData, setFormData] = useState({
    personal_info: {
      fullName: "",
      email: "",
      phone: "",
      gender: "",
      dob: "",
      profilePhoto: null,
    },
    professional_info: {
      specialization: "",
      experience: "",
      qualifications: [],
      hospitalAffiliations: "",
    },
    verification_info: {
      medicalLicense: "",
      documents: [],
    },
  });

  const updateFormData = (section, newData) => {
    setFormData((prevData) => ({
      ...prevData,
      [section]: {
        ...prevData[section],
        ...newData,
      },
    }));
  };

  const nextStep = () => {
    if (validateStep()) setStep(step + 1);
  };

  const prevStep = () => setStep(step - 1);

  const validateStep = () => {
    if (step === 1 && !formData.personal_info.fullName) {
      toast.error("Full Name is required");
      return false;
    }
    if (step === 2 && !formData.professional_info.specialization) {
      toast.error("Specialization is required");
      return false;
    }
    return true;
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch("/api/doctors/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!response.ok) throw new Error("Registration failed");
      toast.success("Doctor registered successfully!");
    } catch (error) {
      toast.error(error.message);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-semibold text-center mb-4">
        Doctor Registration
      </h2>

      {step === 1 && (
        <PersonalInfoForm
          data={formData.personal_info}
          updateData={updateFormData}
        />
      )}
      {step === 2 && (
        <ProfessionalInfoForm
          data={formData.professional_info}
          updateData={updateFormData}
        />
      )}
      {step === 3 && (
        <VerificationInfoForm
          data={formData.verification_info}
          updateData={updateFormData}
        />
      )}

      <div className="flex justify-between mt-6">
        {step > 1 && (
          <button
            onClick={prevStep}
            className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            Previous
          </button>
        )}
        {step < 3 ? (
          <button
            onClick={nextStep}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          >
            Next
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Submit
          </button>
        )}
      </div>
    </div>
  );
};

export default DoctorRegistration;
