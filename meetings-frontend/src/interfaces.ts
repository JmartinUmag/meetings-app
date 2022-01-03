export interface Token {
  accessToken: string
  tokenType: string
}

export interface apiError {
  status: number
  message: string
}

export interface Role {
  id: number
  name: string
}

export interface FileType {
  id: number
  name: string
  path: string
}

interface UserBase {
  username: string
  fullname: string
}

// interface to get users from the api
export interface User extends UserBase {
  id: number
  enabled: boolean
  roles?: Role[]
}

interface MeetingBase {
  title: string
  summary: string
  details: string
  datetime: string | Date
  place: string
}

export interface Meeting extends MeetingBase {
  id: number
  assistants: User[]
  files: FileType[]
}

export interface MeetingCreate extends MeetingBase {
  assistantsIds: number[]
}

export interface MeetingFormData {
  meeting: MeetingCreate
  assistants: User[]
  files: File[]
}
