import api from './api';

export interface Resume {
  id: number;
  filename: string;
  score: number | null;
  uploadDate: string;
  feedback?: Record<string, string>;
  categoryScores?: Record<string, number>;
}

const ResumeService = {
  /**
   * Get all resumes for the current user
   * @returns Promise with array of resumes
   */
  getResumes: async (): Promise<Resume[]> => {
    try {
      // In a real app, this would be a real API call
      // const response = await api.get('/resumes');
      // return response.data;
      
      // Mock response for now
      return new Promise((resolve) => {
        setTimeout(() => {
          const mockResumes: Resume[] = [
            {
              id: 1,
              filename: 'resume_2023.pdf',
              score: 85,
              uploadDate: '2023-05-01',
            },
            {
              id: 2,
              filename: 'resume_2022.pdf',
              score: 72,
              uploadDate: '2022-12-15',
            },
            {
              id: 3,
              filename: 'resume_2021.pdf',
              score: 65,
              uploadDate: '2021-10-20',
            },
          ];
          
          resolve(mockResumes);
        }, 1000);
      });
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Get a resume by ID
   * @param id Resume ID
   * @returns Promise with resume data
   */
  getResumeById: async (id: string | number): Promise<Resume> => {
    try {
      // In a real app, this would be a real API call
      // const response = await api.get(`/resumes/${id}`);
      // return response.data;
      
      // Mock response for now
      return new Promise((resolve) => {
        setTimeout(() => {
          const mockResume: Resume = {
            id: Number(id),
            filename: 'resume_2023.pdf',
            score: 85,
            uploadDate: '2023-05-01',
            feedback: {
              technical_skills: 'Excellent technical skills section. Your skills are well-aligned with industry demands.',
              education: 'Education section is well-presented with relevant details.',
              experience: 'Strong experience section with clear accomplishments and responsibilities.',
              achievements: 'Good achievements, but try to quantify your impact more clearly.',
              formatting: 'Resume is well-formatted and easy to read.',
            },
            categoryScores: {
              technical_skills: 90,
              education: 85,
              experience: 88,
              achievements: 75,
              formatting: 82,
            },
          };
          
          resolve(mockResume);
        }, 1000);
      });
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Upload a new resume
   * @param file Resume file
   * @returns Promise with the created resume
   */
  uploadResume: async (file: File): Promise<Resume> => {
    try {
      // In a real app, this would be a real API call
      // const formData = new FormData();
      // formData.append('file', file);
      // const response = await api.post('/resumes/upload', formData, {
      //   headers: {
      //     'Content-Type': 'multipart/form-data',
      //   },
      // });
      // return response.data;
      
      // Mock response for now
      return new Promise((resolve) => {
        setTimeout(() => {
          const mockResume: Resume = {
            id: Math.floor(Math.random() * 1000),
            filename: file.name,
            score: null,
            uploadDate: new Date().toISOString().split('T')[0],
          };
          
          resolve(mockResume);
        }, 2000);
      });
    } catch (error) {
      throw error;
    }
  },
  
  /**
   * Analyze a resume
   * @param id Resume ID
   * @returns Promise with the analyzed resume
   */
  analyzeResume: async (id: string | number): Promise<Resume> => {
    try {
      // In a real app, this would be a real API call
      // const response = await api.post(`/resumes/${id}/analyze`);
      // return response.data;
      
      // Mock response for now
      return new Promise((resolve) => {
        setTimeout(() => {
          const mockResume: Resume = {
            id: Number(id),
            filename: 'resume_2023.pdf',
            score: 85,
            uploadDate: new Date().toISOString().split('T')[0],
            feedback: {
              technical_skills: 'Excellent technical skills section. Your skills are well-aligned with industry demands.',
              education: 'Education section is well-presented with relevant details.',
              experience: 'Strong experience section with clear accomplishments and responsibilities.',
              achievements: 'Good achievements, but try to quantify your impact more clearly.',
              formatting: 'Resume is well-formatted and easy to read.',
            },
            categoryScores: {
              technical_skills: 90,
              education: 85,
              experience: 88,
              achievements: 75,
              formatting: 82,
            },
          };
          
          resolve(mockResume);
        }, 2000);
      });
    } catch (error) {
      throw error;
    }
  },
};

export default ResumeService;
