#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  4 01:06:31 2019

@author: DanHirst
"""
from JobClasses import Job, Tag


# TODO: Identify whether position is job, internship, job
def jobCategory(job):
    if 'intern' in job.title:
        return Tag('category', 'internship')
    if 'contract' in job.title:
        return Tag('category', 'contractor')

    return Tag('category', 'job')
