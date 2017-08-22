import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  
  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]

  for i in range(num_train):
    scores = X[i].dot(W)
    scores = np.exp(scores)
    
    sum_exp = np.sum(scores)
    
    # normalise
    norm_scores = scores[y[i]] / sum_exp 
    
    loss += -np.log(norm_scores)
    
    # calculate gradients
    for j in range(num_classes):
      dW[:,j] += 1.0 / sum_exp * scores[j] * X[i,:]
      if j == y[i]:
        dW[:,j] -= X[i,:]
    
  loss /= num_train
  dW /= num_train

  loss += 0.5 * reg * np.sum(W * W)
  dW += reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  
  num_classes = W.shape[1]
  num_train = X.shape[0]
  scores = X.dot(W) # N*c array
  exp_scores = np.exp(scores) # N*c array
  sum_exp = np.sum(exp_scores, 1) # N*1 array
  correct_class_exp_scores = exp_scores[np.arange(0, scores.shape[0]), y] # N*1 array
  norm_scores = correct_class_exp_scores / sum_exp # N*1 array
  loss = -np.sum(np.log(norm_scores))

  den_exp_scores = 1.0 / (sum_exp + 1e-8)
  dW = den_exp_scores * exp_scores.T
  dW = dW.dot(X)
  dW = dW.T
  correct_part = np.zeros(scores.shape)
  correct_part[range(num_train), y] = 1
  dW -= X.T.dot(correct_part)  

  loss /= float(num_train)
  dW /= float(num_train)

  loss += 0.5 * reg * np.sum(W * W)
  dW += reg * W
  
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

