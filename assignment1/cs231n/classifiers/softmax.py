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
    num_classes = W.shape[1]
    num_train = X.shape[0]
    for i in range(num_train):
        softmax = X[i].dot(W)
        softmax = np.exp(softmax - np.max(softmax, axis=0))
        probs = softmax / np.sum(softmax)
        loss += -1 * np.log(probs[y[i]])
        
        for j in range(num_classes):
            dW[:, j] += probs[j] * X[i]
            if j == y[i]:
                dW[:, j] += - X[i]
            dW[:, j] += 2 * reg * W[:, j]

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train
    dW /= num_train

    # Add regularization to the loss.
    loss += reg * np.sum(W * W)
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
    num_train = X.shape[0]
    softmax = np.dot(X, W)
    softmax = np.exp(softmax - np.max(softmax, axis=1, keepdims=True))
    probs = softmax / np.sum(softmax, axis=1, keepdims=True)
    vals = -1 * np.log(probs[np.arange(num_train), y])
    loss = np.sum(vals)
    probs[np.arange(num_train), y] += -1
    dW = np.dot(X.T, probs)

    loss /= num_train
    dW /= num_train
    dW += 2 * reg * W

    loss += reg * np.sum(W * W)
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################

    return loss, dW
